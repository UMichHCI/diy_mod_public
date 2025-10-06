#!/usr/bin/env python3
"""
Generate three types of comparison feeds from a comparison template:
1. winner_v_top3.json - Winners vs Top3 losers
2. winner_v_45.json - Winners vs Beyond-Top3 losers (next2)
3. winner_vs_mixed.json - Winners vs Mixed (random from both categories)
"""

import json
import random
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional


def load_comparison_template(file_path: str) -> Dict:
    """Load the comparison template JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading template: {e}")
        sys.exit(1)


def pick_random_from_list(options: List[str], exclude: Optional[str] = None) -> Optional[str]:
    """Pick a random item from list, excluding specified item"""
    available = [item for item in options if item != exclude]
    return random.choice(available) if available else None


def generate_winner_v_top3(template: Dict, output_path: Path) -> None:
    """Generate feed with winners vs top3 losers"""
    print("📋 Generating winner_v_top3.json...")
    
    feed = template.copy()
    feed["metadata"]["feed_type"] = "winner_v_top3"
    feed["metadata"]["description"] = "System winners vs Top3 losers comparison"
    
    posts_modified = 0
    
    for post in feed["posts"]:
        intervention_options = post.get("intervention_options", {})
        current_winner = intervention_options.get("current_winner")
        top3_losers = intervention_options.get("all_top3", [])
        
        if current_winner and top3_losers:
            # Pick random from top3_losers (excluding winner, though it shouldn't be there)
            selected_loser = pick_random_from_list(top3_losers, exclude=current_winner)
            if selected_loser:
                post["image_intervention"] = selected_loser
                posts_modified += 1
                print(f"  📝 Post {post['id']}: {current_winner} → {selected_loser} (top3)")
    
    # Save to file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(feed, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ Generated {output_path} ({posts_modified} posts modified)")


def generate_winner_v_45(template: Dict, output_path: Path) -> None:
    """Generate feed with winners vs beyond-top3 losers (positions 4-5)"""
    print("📋 Generating winner_v_45.json...")
    
    feed = template.copy()
    feed["metadata"]["feed_type"] = "winner_v_45"
    feed["metadata"]["description"] = "System winners vs Beyond-Top3 losers (4-5) comparison"
    
    posts_modified = 0
    
    for post in feed["posts"]:
        intervention_options = post.get("intervention_options", {})
        current_winner = intervention_options.get("current_winner")
        beyond_top3_losers = intervention_options.get("all_next2", [])
        post["text_filter"] = pick_random_from_list(["blur", "overlay", "rewrite"])
        if current_winner and beyond_top3_losers:
            # Pick random from beyond_top3_losers
            selected_loser = pick_random_from_list(beyond_top3_losers, exclude=current_winner)
            if selected_loser:
                post["image_intervention"] = selected_loser
                posts_modified += 1
                print(f"  📝 Post {post['id']}: {current_winner} → {selected_loser} (4-5)")
    
    # Save to file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(feed, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ Generated {output_path} ({posts_modified} posts modified)")


def generate_winner_vs_mixed(template: Dict, output_path: Path) -> None:
    """Generate feed with winners vs mixed losers (random from both categories)"""
    print("📋 Generating winner_vs_mixed.json...")
    
    feed = template.copy()
    feed["metadata"]["feed_type"] = "winner_vs_mixed"
    feed["metadata"]["description"] = "System winners vs Mixed losers (random from top3 + 4-5) comparison"
    
    posts_modified = 0
    
    for post in feed["posts"]:
        intervention_options = post.get("intervention_options", {})
        current_winner = intervention_options.get("current_winner")
        top3_losers = intervention_options.get("all_top3", [])
        beyond_top3_losers = intervention_options.get("all_next2", [])
        
        if current_winner and (top3_losers or beyond_top3_losers):
            # Combine both categories
            all_losers = top3_losers + beyond_top3_losers
            selected_loser = pick_random_from_list(all_losers, exclude=current_winner)
            
            if selected_loser:
                post["image_intervention"] = selected_loser
                posts_modified += 1
                
                # Determine source category for logging
                source = "top3" if selected_loser in top3_losers else "4-5"
                print(f"  📝 Post {post['id']}: {current_winner} → {selected_loser} ({source})")
    
    # Save to file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(feed, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ Generated {output_path} ({posts_modified} posts modified)")


def generate_all_comparison_feeds(template_file: str, output_dir: Optional[str] = None) -> None:
    """Generate all three comparison feed types"""
    template_path = Path(template_file)
    
    # Determine output directory
    if output_dir:
        out_dir = Path(output_dir)
    else:
        out_dir = template_path.parent  # Same directory as template
    
    out_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("COMPARISON FEED GENERATOR")
    print("=" * 70)
    print(f"Template: {template_path}")
    print(f"Output dir: {out_dir}")
    
    # Load template
    template = load_comparison_template(template_file)
    
    # Check if template has the required structure
    posts_with_options = sum(1 for post in template.get("posts", []) 
                           if post.get("intervention_options"))
    
    print(f"📊 Found {posts_with_options} posts with intervention options")
    
    if posts_with_options == 0:
        print("⚠️  No posts with intervention options found. Make sure to use a comparison template generated by process_json_custom_feed.py")
        return
    
    # Generate all three feeds
    generate_winner_v_top3(template, out_dir / "winner_v_top3.json")
    generate_winner_v_45(template, out_dir / "winner_v_45.json")  
    generate_winner_vs_mixed(template, out_dir / "winner_vs_mixed.json")
    
    print("\n" + "=" * 70)
    print("COMPARISON FEEDS GENERATED")
    print("=" * 70)
    print("Next steps:")
    print("1. Run process_json_custom_feed.py with each generated file to create comparison feeds")
    print("2. Use --user-email and --save to store in database for comparison studies")
    print("3. All feeds will share the same session_id for easy grouping")


def main():
    parser = argparse.ArgumentParser(
        description='Generate comparison feeds from a comparison template',
        epilog='''
Examples:
  # Generate in same directory as template
  python generate_comparison_feeds.py comparison_template_abc123.json
  
  # Generate in specific directory  
  python generate_comparison_feeds.py comparison_template_abc123.json --output-dir ./study_feeds/
  
  # Generate from user-specific template
  python generate_comparison_feeds.py phase-two-feed-data/user@example.com/comparison_template_abc123.json
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'template_file',
        help='Path to the comparison template JSON file'
    )
    parser.add_argument(
        '--output-dir',
        help='Directory to save generated comparison feeds (defaults to template directory)'
    )
    
    args = parser.parse_args()
    
    # Check if template file exists
    if not Path(args.template_file).exists():
        print(f"❌ Template file not found: {args.template_file}")
        sys.exit(1)
    
    # Generate comparison feeds
    generate_all_comparison_feeds(args.template_file, args.output_dir)


if __name__ == "__main__":
    main()