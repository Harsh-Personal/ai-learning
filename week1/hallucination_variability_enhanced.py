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


def ask_llm(prompt, temperature, times):
    """Call LLM multiple times and collect responses"""
    all_responses = []
    for i in range(times):
        print(f"  Calling API {i+1}/{times}... ", end="", flush=True)
        try:
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=temperature,
            )
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

    # Similarity analysis
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
        if avg_similarity > 80:
            consistency = "VERY HIGH - Near deterministic"
        elif avg_similarity > 50:
            consistency = "MODERATE - Some variation"
        elif avg_similarity > 20:
            consistency = "LOW - Significant variation"
        else:
            consistency = "VERY LOW - Highly variable"

        print(f"  🎯 Consistency Level: {consistency}")

    return {
        "label": label,
        "avg_similarity": sum(similarities) / len(similarities) if similarities else 0,
        "avg_length": sum(lengths) / len(lengths),
        "avg_tokens": sum(tokens) / len(tokens) if tokens else 0,
        "responses": valid_responses,
    }


def run_temperature_experiment(prompt, temperatures=[0, 1], calls_per_temp=10):
    """Run complete temperature experiment"""
    print(f"\n{'='*70}")
    print(f"STARTING TEMPERATURE EXPERIMENT")
    print("=" * 70)
    print(f'Prompt: "{prompt}"')
    print(f"Temperatures to test: {temperatures}")
    print(f"Calls per temperature: {calls_per_temp}")
    print(f"Total API calls: {len(temperatures) * calls_per_temp}")

    results = {}

    for temp in temperatures:
        print(f"\n{'='*70}")
        print(f"🌡️  TESTING TEMPERATURE = {temp}")
        print("=" * 70)

        responses = ask_llm(prompt, temp, calls_per_temp)
        analysis = analyze_responses(responses, f"Temperature {temp}")
        if analysis:
            results[f"temp_{temp}"] = analysis

    # Comparative analysis
    print(f"\n{'='*70}")
    print(f"COMPARATIVE RESULTS")
    print("=" * 70)

    for temp in temperatures:
        key = f"temp_{temp}"
        if key in results:
            print(f"\nTemperature {temp}:")
            print(f"  Average Similarity: {results[key]['avg_similarity']:.2f}%")
            print(f"  Average Length: {results[key]['avg_length']:.0f} chars")
            if results[key]["avg_tokens"] > 0:
                print(f"  Average Tokens: {results[key]['avg_tokens']:.0f}")

    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"llm_temperature_experiment_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Results saved to: {filename}")

    return results


# Main execution
if __name__ == "__main__":
    # Run the temperature experiment
    results = run_temperature_experiment(
        prompt="explain how testing is done in AI",
        temperatures=[0, 1],
        calls_per_temp=10,
    )

    # Optional: Test with different prompts
    # results2 = run_temperature_experiment(
    #     prompt="what is a neural network?",
    #     temperatures=[0, 0.5, 1],
    #     calls_per_temp=5
    # )
