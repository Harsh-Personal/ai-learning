import os
import time
import json
from datetime import datetime
from difflib import SequenceMatcher
from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


def calculate_similarity(text1, text2):
    """Calculate similarity percentage between two texts"""
    return SequenceMatcher(None, text1, text2).ratio() * 100


def ask_llm_with_seed(prompt, temperature, times, seed=None):
    """
    Call LLM multiple times with optional seed parameter
    
    Args:
        prompt: The question to ask
        temperature: Temperature setting (0-2)
        times: Number of times to call the API
        seed: Optional seed for reproducibility (e.g., 42)
    """
    all_responses = []
    for i in range(times):
        print(f"  Calling API {i+1}/{times}... ", end="", flush=True)
        try:
            # Build the API call parameters
            api_params = {
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                "model": "llama-3.3-70b-versatile",
                "temperature": temperature,
            }
            
            # Add seed if provided
            if seed is not None:
                api_params["seed"] = seed
            
            response = client.chat.completions.create(**api_params)
            
            content = response.choices[0].message.content
            tokens_used = (
                response.usage.total_tokens if hasattr(response, "usage") else 0
            )

            all_responses.append(
                {
                    "response_num": i + 1,
                    "content": content,
                    "length": len(content),
                    "tokens": tokens_used,
                    "seed": seed,
                    "timestamp": datetime.now().isoformat(),
                }
            )
            print(f"✓ ({len(content)} chars, {tokens_used} tokens)")
            time.sleep(2)  # Rate limiting

        except Exception as e:
            print(f"✗ Error: {str(e)}")
            all_responses.append(
                {
                    "response_num": i + 1,
                    "error": str(e),
                    "seed": seed,
                    "timestamp": datetime.now().isoformat(),
                }
            )

    return all_responses


def analyze_responses(responses, label):
    """Analyze consistency and variability of responses"""
    print(f"\n{'='*70}")
    print(f"ANALYSIS: {label}")
    print("=" * 70)

    valid_responses = [r for r in responses if "error" not in r]

    if len(valid_responses) < 2:
        print("Not enough valid responses for analysis")
        return None

    # Basic stats
    lengths = [r["length"] for r in valid_responses]
    tokens = [r["tokens"] for r in valid_responses if r["tokens"] > 0]

    print(f"\n📊 Response Statistics:")
    print(f"  Total responses: {len(valid_responses)}")
    print(f"  Avg length: {sum(lengths)/len(lengths):.0f} characters")
    print(f"  Min length: {min(lengths)} characters")
    print(f"  Max length: {max(lengths)} characters")
    print(f"  Length variance: {max(lengths) - min(lengths)} characters")

    if tokens:
        print(f"  Avg tokens: {sum(tokens)/len(tokens):.0f}")
        print(f"  Total tokens used: {sum(tokens)}")

    # Similarity analysis - compare all responses to each other
    print(f"\n🔍 Similarity Analysis (comparing all to Response 1):")
    base_content = valid_responses[0]["content"]
    similarities = []

    for i, resp in enumerate(valid_responses[1:], start=2):
        similarity = calculate_similarity(base_content, resp["content"])
        similarities.append(similarity)
        emoji = "✅" if similarity > 80 else "⚠️" if similarity > 50 else "❌"
        print(f"  {emoji} Response 1 vs {i}: {similarity:.2f}%")

    if similarities:
        avg_similarity = sum(similarities) / len(similarities)
        print(f"\n  📈 Average Similarity: {avg_similarity:.2f}%")

        # Interpretation
        if avg_similarity > 95:
            consistency = "PERFECT - Deterministic (likely identical)"
        elif avg_similarity > 80:
            consistency = "VERY HIGH - Near deterministic"
        elif avg_similarity > 50:
            consistency = "MODERATE - Some variation"
        elif avg_similarity > 20:
            consistency = "LOW - Significant variation"
        else:
            consistency = "VERY LOW - Highly variable"

        print(f"  🎯 Consistency Level: {consistency}")

    # Check if all responses are identical
    all_identical = all(r["content"] == valid_responses[0]["content"] for r in valid_responses)
    if all_identical:
        print(f"\n  🎉 ALL RESPONSES ARE IDENTICAL!")

    return {
        "label": label,
        "avg_similarity": sum(similarities) / len(similarities) if similarities else 0,
        "avg_length": sum(lengths) / len(lengths),
        "avg_tokens": sum(tokens) / len(tokens) if tokens else 0,
        "all_identical": all_identical,
        "responses": valid_responses,
    }


def run_seed_experiment(prompt, temperature=0, calls_per_test=10):
    """
    Run experiment to compare:
    1. Temperature=0 WITHOUT seed
    2. Temperature=0 WITH seed=42
    3. Temperature=0 WITH seed=123 (different seed)
    """
    print(f"\n{'='*70}")
    print(f"🌱 SEED IMPACT EXPERIMENT")
    print("=" * 70)
    print(f'Prompt: "{prompt}"')
    print(f"Temperature: {temperature}")
    print(f"Calls per test: {calls_per_test}")
    print(f"Total API calls: {calls_per_test * 3}")
    print("\nWe will test:")
    print("  1️⃣  Temperature=0, NO seed (baseline)")
    print("  2️⃣  Temperature=0, seed=42")
    print("  3️⃣  Temperature=0, seed=123 (different seed)")

    results = {}

    # Test 1: No seed
    print(f"\n{'='*70}")
    print(f"1️⃣  TESTING: Temperature={temperature}, NO SEED")
    print("=" * 70)
    print("Expected: Some variation even at temp=0")
    
    responses_no_seed = ask_llm_with_seed(prompt, temperature, calls_per_test, seed=None)
    analysis_no_seed = analyze_responses(responses_no_seed, f"Temp={temperature}, No Seed")
    if analysis_no_seed:
        results["no_seed"] = analysis_no_seed

    # Test 2: With seed=42
    print(f"\n{'='*70}")
    print(f"2️⃣  TESTING: Temperature={temperature}, SEED=42")
    print("=" * 70)
    print("Expected: High consistency, possibly identical responses")
    
    responses_seed_42 = ask_llm_with_seed(prompt, temperature, calls_per_test, seed=42)
    analysis_seed_42 = analyze_responses(responses_seed_42, f"Temp={temperature}, Seed=42")
    if analysis_seed_42:
        results["seed_42"] = analysis_seed_42

    # Test 3: With seed=123 (different seed)
    print(f"\n{'='*70}")
    print(f"3️⃣  TESTING: Temperature={temperature}, SEED=123")
    print("=" * 70)
    print("Expected: High consistency, but different from seed=42")
    
    responses_seed_123 = ask_llm_with_seed(prompt, temperature, calls_per_test, seed=123)
    analysis_seed_123 = analyze_responses(responses_seed_123, f"Temp={temperature}, Seed=123")
    if analysis_seed_123:
        results["seed_123"] = analysis_seed_123

    # Comparative analysis
    print(f"\n{'='*70}")
    print(f"📊 COMPARATIVE RESULTS - SEED IMPACT")
    print("=" * 70)

    print("\n🔬 Consistency Comparison:")
    if "no_seed" in results:
        print(f"\n  No Seed:")
        print(f"    Average Similarity: {results['no_seed']['avg_similarity']:.2f}%")
        print(f"    All Identical: {'Yes ✅' if results['no_seed']['all_identical'] else 'No ❌'}")
    
    if "seed_42" in results:
        print(f"\n  Seed=42:")
        print(f"    Average Similarity: {results['seed_42']['avg_similarity']:.2f}%")
        print(f"    All Identical: {'Yes ✅' if results['seed_42']['all_identical'] else 'No ❌'}")
    
    if "seed_123" in results:
        print(f"\n  Seed=123:")
        print(f"    Average Similarity: {results['seed_123']['avg_similarity']:.2f}%")
        print(f"    All Identical: {'Yes ✅' if results['seed_123']['all_identical'] else 'No ❌'}")

    # Compare seed=42 vs seed=123 (should be different)
    if "seed_42" in results and "seed_123" in results:
        cross_similarity = calculate_similarity(
            results["seed_42"]["responses"][0]["content"],
            results["seed_123"]["responses"][0]["content"]
        )
        print(f"\n🔀 Cross-Seed Comparison:")
        print(f"  Seed=42 vs Seed=123: {cross_similarity:.2f}%")
        print(f"  (Different seeds should produce different but consistent outputs)")

    # Key insights
    print(f"\n{'='*70}")
    print(f"💡 KEY INSIGHTS")
    print("=" * 70)
    
    if "no_seed" in results and "seed_42" in results:
        improvement = results["seed_42"]["avg_similarity"] - results["no_seed"]["avg_similarity"]
        print(f"\n1. Seed Impact on Consistency:")
        print(f"   Without seed: {results['no_seed']['avg_similarity']:.2f}% similarity")
        print(f"   With seed=42: {results['seed_42']['avg_similarity']:.2f}% similarity")
        print(f"   Improvement: {improvement:+.2f}% {'📈' if improvement > 0 else '📉'}")
        
        if results["seed_42"]["all_identical"]:
            print(f"\n2. ✅ Seed=42 produced IDENTICAL responses!")
            print(f"   This means perfect reproducibility for testing/evaluation")
        else:
            print(f"\n2. ⚠️  Seed=42 did not produce identical responses")
            print(f"   But consistency improved significantly")
    
    print(f"\n3. Use Cases:")
    print(f"   • Testing/Evaluation: Use seed for reproducible results")
    print(f"   • Production: No seed for more diverse outputs")
    print(f"   • A/B Testing: Use different seeds to test variations")

    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"seed_impact_experiment_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Results saved to: {filename}")

    return results


# Main execution
if __name__ == "__main__":
    # Run the seed impact experiment
    results = run_seed_experiment(
        prompt="explain how testing is done in AI",
        temperature=0,
        calls_per_test=10,
    )

    # Optional: Test with a simpler prompt to see if results differ
    # results2 = run_seed_experiment(
    #     prompt="what is 2+2?",
    #     temperature=0,
    #     calls_per_test=5,
    # )
