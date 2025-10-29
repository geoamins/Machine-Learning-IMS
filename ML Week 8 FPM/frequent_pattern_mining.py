"""
Frequent Pattern Mining Algorithms: Apriori and FP-Growth
=========================================================

This module provides comprehensive implementations and examples of:
1. Apriori Algorithm
2. FP-Growth Algorithm

Author: Dr. Adnan Amin
Course: Machine Learning Crash Course
"""

import pandas as pd
import numpy as np
from collections import defaultdict, Counter
from itertools import combinations
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Set, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

class AprioriAlgorithm:
    """
    Apriori Algorithm for Frequent Pattern Mining
    
    The Apriori algorithm uses a "bottom-up" approach where frequent subsets 
    are extended one item at a time (a step known as candidate generation), 
    and groups of candidates are tested against the data.
    """
    
    def __init__(self, min_support: float = 0.3):
        """
        Initialize Apriori Algorithm
        
        Args:
            min_support: Minimum support threshold (0.0 to 1.0)
        """
        self.min_support = min_support
        self.frequent_itemsets = {}
        self.rules = []
        
    def _get_frequent_1_itemsets(self, transactions: List[List[str]]) -> Dict[frozenset, int]:
        """Find frequent 1-itemsets"""
        item_counts = Counter()
        for transaction in transactions:
            for item in transaction:
                item_counts[item] += 1
        
        min_count = int(self.min_support * len(transactions))
        frequent_1_itemsets = {}
        
        for item, count in item_counts.items():
            if count >= min_count:
                frequent_1_itemsets[frozenset([item])] = count
                
        return frequent_1_itemsets
    
    def _generate_candidates(self, frequent_itemsets: Dict[frozenset, int], k: int) -> Set[frozenset]:
        """Generate candidate k-itemsets from frequent (k-1)-itemsets"""
        candidates = set()
        itemsets = list(frequent_itemsets.keys())
        
        for i in range(len(itemsets)):
            for j in range(i + 1, len(itemsets)):
                # Join step: combine two (k-1)-itemsets
                union = itemsets[i] | itemsets[j]
                if len(union) == k:
                    # Prune step: check if all (k-1)-subsets are frequent
                    subsets = [frozenset(subset) for subset in combinations(union, k-1)]
                    if all(subset in frequent_itemsets for subset in subsets):
                        candidates.add(union)
        
        return candidates
    
    def _count_support(self, candidates: Set[frozenset], transactions: List[List[str]]) -> Dict[frozenset, int]:
        """Count support for candidate itemsets"""
        counts = defaultdict(int)
        
        for transaction in transactions:
            transaction_set = set(transaction)
            for candidate in candidates:
                if candidate.issubset(transaction_set):
                    counts[candidate] += 1
        
        return dict(counts)
    
    def fit(self, transactions: List[List[str]]) -> Dict[int, Dict[frozenset, int]]:
        """
        Run Apriori algorithm to find frequent itemsets
        
        Args:
            transactions: List of transactions, each transaction is a list of items
            
        Returns:
            Dictionary with frequent itemsets by size
        """
        print("Running Apriori Algorithm...")
        print(f"Minimum Support: {self.min_support}")
        print(f"Number of Transactions: {len(transactions)}")
        print("-" * 50)
        
        # Find frequent 1-itemsets
        frequent_itemsets = self._get_frequent_1_itemsets(transactions)
        self.frequent_itemsets[1] = frequent_itemsets
        
        print(f"Frequent 1-itemsets: {len(frequent_itemsets)}")
        for itemset, count in frequent_itemsets.items():
            print(f"  {list(itemset)}: support = {count}")
        
        k = 2
        while frequent_itemsets:
            print(f"\nGenerating {k}-itemsets...")
            
            # Generate candidates
            candidates = self._generate_candidates(frequent_itemsets, k)
            print(f"  Generated {len(candidates)} candidates")
            
            if not candidates:
                break
                
            # Count support
            candidate_counts = self._count_support(candidates, transactions)
            
            # Filter frequent itemsets
            min_count = int(self.min_support * len(transactions))
            frequent_itemsets = {itemset: count for itemset, count in candidate_counts.items() 
                               if count >= min_count}
            
            if frequent_itemsets:
                self.frequent_itemsets[k] = frequent_itemsets
                print(f"  Frequent {k}-itemsets: {len(frequent_itemsets)}")
                for itemset, count in frequent_itemsets.items():
                    print(f"    {list(itemset)}: support = {count}")
            else:
                print(f"  No frequent {k}-itemsets found")
                break
                
            k += 1
        
        return self.frequent_itemsets
    
    def generate_rules(self, min_confidence: float = 0.5) -> List[Tuple[frozenset, frozenset, float, float]]:
        """
        Generate association rules from frequent itemsets
        
        Args:
            min_confidence: Minimum confidence threshold
            
        Returns:
            List of rules (antecedent, consequent, support, confidence)
        """
        print(f"\nGenerating Association Rules (min_confidence = {min_confidence})...")
        print("-" * 50)
        
        rules = []
        
        for k in range(2, len(self.frequent_itemsets) + 1):
            if k not in self.frequent_itemsets:
                continue
                
            for itemset in self.frequent_itemsets[k]:
                itemset_support = self.frequent_itemsets[k][itemset]
                
                # Generate all possible rules from this itemset
                for i in range(1, len(itemset)):
                    for antecedent in combinations(itemset, i):
                        antecedent = frozenset(antecedent)
                        consequent = itemset - antecedent
                        
                        # Find antecedent support
                        antecedent_support = None
                        for size in self.frequent_itemsets:
                            if antecedent in self.frequent_itemsets[size]:
                                antecedent_support = self.frequent_itemsets[size][antecedent]
                                break
                        
                        if antecedent_support:
                            confidence = itemset_support / antecedent_support
                            if confidence >= min_confidence:
                                support = itemset_support
                                rules.append((antecedent, consequent, support, confidence))
        
        # Sort by confidence
        rules.sort(key=lambda x: x[3], reverse=True)
        
        print(f"Generated {len(rules)} rules:")
        for i, (antecedent, consequent, support, confidence) in enumerate(rules[:10]):  # Show top 10
            print(f"  {i+1}. {list(antecedent)} -> {list(consequent)} "
                  f"(support={support}, confidence={confidence:.3f})")
        
        self.rules = rules
        return rules


class FPGrowthAlgorithm:
    """
    FP-Growth Algorithm for Frequent Pattern Mining
    
    FP-Growth uses a compressed representation of the database called FP-tree
    and mines frequent patterns by pattern fragment growth.
    """
    
    def __init__(self, min_support: float = 0.3):
        """
        Initialize FP-Growth Algorithm
        
        Args:
            min_support: Minimum support threshold (0.0 to 1.0)
        """
        self.min_support = min_support
        self.frequent_itemsets = {}
        self.fp_tree = None
        
    class FPNode:
        """Node in FP-Tree"""
        def __init__(self, item: str = None, count: int = 0, parent=None):
            self.item = item
            self.count = count
            self.parent = parent
            self.children = {}
            self.node_link = None  # Link to next node with same item
            
        def __repr__(self):
            return f"FPNode({self.item}, {self.count})"
    
    def _build_header_table(self, transactions: List[List[str]]) -> Dict[str, Tuple[int, Any]]:
        """Build header table with item frequencies"""
        item_counts = Counter()
        for transaction in transactions:
            for item in transaction:
                item_counts[item] += 1
        
        min_count = int(self.min_support * len(transactions))
        header_table = {}
        
        for item, count in item_counts.items():
            if count >= min_count:
                header_table[item] = (count, None)  # (count, node_link)
        
        return header_table
    
    def _build_fp_tree(self, transactions: List[List[str]], header_table: Dict[str, Tuple[int, Any]]) -> Tuple[Any, Dict[str, Tuple[int, Any]]]:
        """Build FP-Tree from transactions"""
        root = self.FPNode()
        
        for transaction in transactions:
            # Filter and sort items by frequency
            filtered_items = [item for item in transaction if item in header_table]
            filtered_items.sort(key=lambda x: header_table[x][0], reverse=True)
            
            if filtered_items:
                self._insert_transaction(root, filtered_items, header_table)
        
        return root, header_table
    
    def _insert_transaction(self, node: FPNode, items: List[str], header_table: Dict[str, Tuple[int, Any]]):
        """Insert a transaction into FP-Tree"""
        if not items:
            return
        
        item = items[0]
        
        if item in node.children:
            node.children[item].count += 1
        else:
            node.children[item] = self.FPNode(item, 1, node)
            
            # Update header table links
            if header_table[item][1] is None:
                header_table[item] = (header_table[item][0], node.children[item])
            else:
                current = header_table[item][1]
                while current.node_link is not None:
                    current = current.node_link
                current.node_link = node.children[item]
        
        # Recursively insert remaining items
        self._insert_transaction(node.children[item], items[1:], header_table)
    
    def _get_conditional_pattern_base(self, item: str, header_table: Dict[str, Tuple[int, Any]]) -> List[List[str]]:
        """Get conditional pattern base for an item"""
        pattern_base = []
        
        if header_table[item][1] is not None:
            node = header_table[item][1]
            while node is not None:
                # Get path from root to this node
                path = []
                current = node.parent
                while current.parent is not None:  # Skip root
                    path.append(current.item)
                    current = current.parent
                
                if path:
                    # Add path with node's count
                    for _ in range(node.count):
                        pattern_base.append(path)
                
                node = node.node_link
        
        return pattern_base
    
    def _mine_fp_tree(self, fp_tree: FPNode, header_table: Dict[str, Tuple[int, Any]], 
                     prefix: List[str], min_count: int) -> Dict[frozenset, int]:
        """Mine frequent patterns from FP-Tree"""
        frequent_patterns = {}
        
        # Sort items by frequency
        items = sorted(header_table.keys(), key=lambda x: header_table[x][0])
        
        for item in items:
            # Create new prefix
            new_prefix = prefix + [item]
            new_prefix_set = frozenset(new_prefix)
            
            # Count support
            support = header_table[item][0]
            frequent_patterns[new_prefix_set] = support
            
            # Get conditional pattern base
            conditional_pattern_base = self._get_conditional_pattern_base(item, header_table)
            
            if conditional_pattern_base:
                # Build conditional FP-Tree
                conditional_header_table = self._build_header_table(conditional_pattern_base)
                conditional_fp_tree, conditional_header_table = self._build_fp_tree(
                    conditional_pattern_base, conditional_header_table)
                
                # Recursively mine conditional FP-Tree
                conditional_patterns = self._mine_fp_tree(
                    conditional_fp_tree, conditional_header_table, new_prefix, min_count)
                
                frequent_patterns.update(conditional_patterns)
        
        return frequent_patterns
    
    def fit(self, transactions: List[List[str]]) -> Dict[int, Dict[frozenset, int]]:
        """
        Run FP-Growth algorithm to find frequent itemsets
        
        Args:
            transactions: List of transactions, each transaction is a list of items
            
        Returns:
            Dictionary with frequent itemsets grouped by size
        """
        print("Running FP-Growth Algorithm...")
        print(f"Minimum Support: {self.min_support}")
        print(f"Number of Transactions: {len(transactions)}")
        print("-" * 50)
        
        min_count = int(self.min_support * len(transactions))
        
        # Build header table
        header_table = self._build_header_table(transactions)
        print(f"Frequent items: {len(header_table)}")
        for item, (count, _) in header_table.items():
            print(f"  {item}: support = {count}")
        
        # Build FP-Tree
        fp_tree, header_table = self._build_fp_tree(transactions, header_table)
        self.fp_tree = fp_tree
        
        # Mine FP-Tree
        frequent_patterns = self._mine_fp_tree(fp_tree, header_table, [], min_count)
        
        # Group by size
        self.frequent_itemsets = {}
        for itemset, support in frequent_patterns.items():
            size = len(itemset)
            if size not in self.frequent_itemsets:
                self.frequent_itemsets[size] = {}
            self.frequent_itemsets[size][itemset] = support
        
        # Display results
        for size in sorted(self.frequent_itemsets.keys()):
            print(f"\nFrequent {size}-itemsets: {len(self.frequent_itemsets[size])}")
            for itemset, support in self.frequent_itemsets[size].items():
                print(f"  {list(itemset)}: support = {support}")
        
        return self.frequent_itemsets


def create_sample_dataset() -> List[List[str]]:
    """
    Create a sample transaction dataset for demonstration
    
    Returns:
        List of transactions
    """
    transactions = [
        ['bread', 'milk'],
        ['bread', 'diaper', 'drink', 'eggs'],
        ['milk', 'diaper', 'drink', 'cola'],
        ['bread', 'milk', 'diaper', 'drink'],
        ['bread', 'milk', 'diaper', 'cola'],
        ['milk', 'diaper', 'cola'],
        ['bread', 'milk', 'cola'],
        ['bread', 'milk', 'diaper', 'drink', 'eggs'],
        ['milk', 'diaper', 'drink', 'eggs'],
        ['bread', 'milk', 'diaper', 'drink']
    ]
    
    return transactions


def visualize_frequent_itemsets(frequent_itemsets: Dict[int, Dict[frozenset, int]], 
                              algorithm_name: str):
    """
    Visualize frequent itemsets
    
    Args:
        frequent_itemsets: Dictionary with frequent itemsets by size
        algorithm_name: Name of the algorithm for title
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle(f'Frequent Itemsets Analysis - {algorithm_name}', fontsize=16)
    
    # Plot 1: Number of frequent itemsets by size
    sizes = list(frequent_itemsets.keys())
    counts = [len(frequent_itemsets[size]) for size in sizes]
    
    axes[0, 0].bar(sizes, counts, color='skyblue', alpha=0.7)
    axes[0, 0].set_xlabel('Itemset Size')
    axes[0, 0].set_ylabel('Number of Frequent Itemsets')
    axes[0, 0].set_title('Frequent Itemsets Count by Size')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: Support distribution
    all_supports = []
    for size_itemsets in frequent_itemsets.values():
        all_supports.extend(size_itemsets.values())
    
    axes[0, 1].hist(all_supports, bins=10, color='lightgreen', alpha=0.7, edgecolor='black')
    axes[0, 1].set_xlabel('Support Count')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].set_title('Support Distribution')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Itemset size vs average support
    avg_supports = []
    for size in sizes:
        supports = list(frequent_itemsets[size].values())
        avg_supports.append(np.mean(supports))
    
    axes[1, 0].plot(sizes, avg_supports, marker='o', linewidth=2, markersize=8, color='red')
    axes[1, 0].set_xlabel('Itemset Size')
    axes[1, 0].set_ylabel('Average Support')
    axes[1, 0].set_title('Average Support by Itemset Size')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Plot 4: Top 10 most frequent itemsets
    all_itemsets = []
    for size_itemsets in frequent_itemsets.values():
        all_itemsets.extend([(itemset, support) for itemset, support in size_itemsets.items()])
    
    all_itemsets.sort(key=lambda x: x[1], reverse=True)
    top_10 = all_itemsets[:10]
    
    itemset_labels = [', '.join(list(itemset)) for itemset, _ in top_10]
    supports = [support for _, support in top_10]
    
    axes[1, 1].barh(range(len(itemset_labels)), supports, color='orange', alpha=0.7)
    axes[1, 1].set_yticks(range(len(itemset_labels)))
    axes[1, 1].set_yticklabels(itemset_labels)
    axes[1, 1].set_xlabel('Support Count')
    axes[1, 1].set_title('Top 10 Most Frequent Itemsets')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()


def compare_algorithms():
    """
    Compare Apriori and FP-Growth algorithms
    """
    print("=" * 60)
    print("FREQUENT PATTERN MINING ALGORITHMS COMPARISON")
    print("=" * 60)
    
    # Create sample dataset
    transactions = create_sample_dataset()
    
    print("\nSample Transaction Dataset:")
    print("-" * 30)
    for i, transaction in enumerate(transactions, 1):
        print(f"T{i}: {transaction}")
    
    # Test both algorithms
    min_support = 0.3
    
    print("\n" + "=" * 60)
    print("APRIORI ALGORITHM")
    print("=" * 60)
    
    apriori = AprioriAlgorithm(min_support=min_support)
    apriori_results = apriori.fit(transactions)
    
    print("\n" + "=" * 60)
    print("FP-GROWTH ALGORITHM")
    print("=" * 60)
    
    fp_growth = FPGrowthAlgorithm(min_support=min_support)
    fp_growth_results = fp_growth.fit(transactions)
    
    # Generate association rules
    print("\n" + "=" * 60)
    print("ASSOCIATION RULES (Apriori)")
    print("=" * 60)
    
    rules = apriori.generate_rules(min_confidence=0.5)
    
    # Visualizations
    print("\nGenerating visualizations...")
    visualize_frequent_itemsets(apriori_results, "Apriori")
    visualize_frequent_itemsets(fp_growth_results, "FP-Growth")
    
    # Performance comparison
    print("\n" + "=" * 60)
    print("PERFORMANCE COMPARISON")
    print("=" * 60)
    
    apriori_total = sum(len(itemsets) for itemsets in apriori_results.values())
    fp_growth_total = sum(len(itemsets) for itemsets in fp_growth_results.values())
    
    print(f"Apriori - Total frequent itemsets: {apriori_total}")
    print(f"FP-Growth - Total frequent itemsets: {fp_growth_total}")
    print(f"Results match: {apriori_total == fp_growth_total}")
    
    return apriori_results, fp_growth_results, rules


if __name__ == "__main__":
    # Run the comparison
    apriori_results, fp_growth_results, rules = compare_algorithms()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("Both algorithms successfully found frequent patterns!")
    print("Key differences:")
    print("1. Apriori: Generates candidates and tests them against database")
    print("2. FP-Growth: Builds compressed FP-tree and mines patterns recursively")
    print("3. FP-Growth is generally more efficient for large datasets")
    print("4. Both algorithms produce the same results for the same parameters")
