"""
Test script to verify all parsers are working correctly
"""

import asyncio
from pathlib import Path
from src.scanner.parsers import (
    ParserRegistry,
    list_supported_services,
    get_parser
)


async def test_all_parsers():
    """Test all registered parsers"""

    print("=" * 60)
    print("Tokeneyes Parser Test Suite")
    print("=" * 60)
    print()

    # List all supported services
    services = list_supported_services()

    print(f"✅ Total Parsers Registered: {len(services)}")
    print(f"✅ Supported Services: {', '.join(services)}")
    print()

    # Test each parser
    for service in sorted(services):
        print(f"Testing {service.upper()} parser...")

        try:
            parser = get_parser(service)

            if parser:
                print(f"  ✅ Parser loaded: {parser.__class__.__name__}")
                print(f"  ✅ Service name: {parser.service_name}")
                print(f"  ✅ Supported models ({len(parser.supported_models)}):")

                for model in parser.supported_models[:5]:  # Show first 5
                    print(f"     - {model}")

                if len(parser.supported_models) > 5:
                    print(f"     ... and {len(parser.supported_models) - 5} more")
            else:
                print(f"  ❌ Failed to load parser")

        except Exception as e:
            print(f"  ❌ Error: {e}")

        print()

    print("=" * 60)
    print("Parser Coverage Summary")
    print("=" * 60)
    print()

    # Categorize parsers
    phase_1 = ['openai', 'anthropic', 'google', 'github']
    phase_2 = ['deepseek', 'meta', 'mistral']
    phase_3 = ['minimax', 'xai', 'cohere']

    phase_1_found = [s for s in services if s in phase_1]
    phase_2_found = [s for s in services if s in phase_2]
    phase_3_found = [s for s in services if s in phase_3]

    print(f"Phase 1 (P0) - Core Providers:")
    print(f"  Expected: 4, Found: {len(phase_1_found)}")
    print(f"  {', '.join(phase_1_found) if phase_1_found else 'None'}")
    print()

    print(f"Phase 2 (P1) - Major Providers:")
    print(f"  Expected: 3, Found: {len(phase_2_found)}")
    print(f"  {', '.join(phase_2_found) if phase_2_found else 'None'}")
    print()

    print(f"Phase 3 (P2) - Additional Providers:")
    print(f"  Expected: 3, Found: {len(phase_3_found)}")
    print(f"  {', '.join(phase_3_found) if phase_3_found else 'None'}")
    print()

    total_expected = len(phase_1) + len(phase_2) + len(phase_3)
    total_found = len(phase_1_found) + len(phase_2_found) + len(phase_3_found)

    print("=" * 60)
    print(f"Overall Coverage: {total_found}/{total_expected} parsers ({total_found/total_expected*100:.1f}%)")
    print("=" * 60)

    if total_found == total_expected:
        print("✅ All parsers successfully implemented!")
    else:
        print(f"⚠️  Missing {total_expected - total_found} parsers")


if __name__ == '__main__':
    asyncio.run(test_all_parsers())
