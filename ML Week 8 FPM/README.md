# Frequent Pattern Mining: Apriori vs FP-Growth

## Course Materials for Machine Learning Crash Course
### Instructor: Dr. Adnan Amin

---

## Overview

This repository contains comprehensive teaching materials for understanding and implementing frequent pattern mining algorithms, specifically the Apriori and FP-Growth algorithms.

## Files Included

1. **`frequent_pattern_mining.py`** - Complete implementation of both algorithms
2. **`Frequent_Pattern_Mining_Tutorial.ipynb`** - Interactive Jupyter notebook tutorial
3. **`requirements.txt`** - Python dependencies
4. **`README.md`** - This file

## Learning Objectives

Students will learn to:
- Understand the fundamentals of frequent pattern mining
- Implement the Apriori algorithm from scratch
- Implement the FP-Growth algorithm from scratch
- Compare the performance and characteristics of both algorithms
- Generate and interpret association rules
- Visualize frequent patterns and their relationships

## Prerequisites

- Basic knowledge of Python programming
- Understanding of data structures (lists, dictionaries, sets)
- Familiarity with basic probability concepts
- Basic understanding of data mining concepts

## Installation

1. Clone or download this repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch Jupyter Notebook:
   ```bash
   jupyter notebook
   ```
4. Open `Frequent_Pattern_Mining_Tutorial.ipynb`

## Usage

### Running the Python Script
```python
python frequent_pattern_mining.py
```

### Using the Jupyter Notebook
1. Open `Frequent_Pattern_Mining_Tutorial.ipynb` in Jupyter
2. Run cells sequentially to follow the tutorial
3. Experiment with different parameters and datasets

## Algorithm Details

### Apriori Algorithm
- **Approach**: Bottom-up candidate generation
- **Key Steps**: 
  1. Generate frequent 1-itemsets
  2. Generate candidate k-itemsets from frequent (k-1)-itemsets
  3. Prune candidates using Apriori property
  4. Count support for remaining candidates
  5. Filter frequent itemsets
- **Complexity**: O(2^n) in worst case
- **Memory**: High due to candidate generation

### FP-Growth Algorithm
- **Approach**: Pattern growth using FP-Tree
- **Key Steps**:
  1. Build header table with item frequencies
  2. Construct FP-Tree by inserting transactions
  3. Mine FP-Tree recursively using pattern growth
  4. Generate frequent patterns from conditional pattern bases
- **Complexity**: O(n * m) where n is transactions, m is items
- **Memory**: More efficient due to compressed representation

## Sample Dataset

The tutorial uses a sample market basket dataset with the following items:
- bread, milk, diaper, beer, eggs, cola

## Key Concepts Covered

1. **Support**: Frequency of an itemset in the dataset
2. **Confidence**: Probability of consequent given antecedent
3. **Lift**: How much more likely consequent is given antecedent
4. **Frequent Itemset**: Itemset with support above threshold
5. **Association Rule**: Rule of the form A → B

## Exercises

The notebook includes several hands-on exercises:
1. Parameter sensitivity analysis
2. Testing with different datasets
3. Performance comparison
4. Visualization of results

## Expected Outcomes

After completing this tutorial, students should be able to:
- Explain the differences between Apriori and FP-Growth
- Choose the appropriate algorithm for different scenarios
- Implement both algorithms from scratch
- Generate meaningful association rules
- Interpret and visualize frequent patterns

## Extensions

Students can extend this work by:
- Implementing parallel versions of the algorithms
- Exploring closed and maximal frequent itemsets
- Testing on larger, real-world datasets
- Implementing additional pruning techniques
- Adding support for different data types

## References

1. Agrawal, R., & Srikant, R. (1994). Fast algorithms for mining association rules. VLDB.
2. Han, J., Pei, J., & Yin, Y. (2000). Mining frequent patterns without candidate generation. SIGMOD.
3. Tan, P. N., Steinbach, M., & Kumar, V. (2018). Introduction to Data Mining. Pearson.

## Contact

For questions or clarifications, please contact Dr. Adnan Amin.

---

**Note**: This material is designed for educational purposes. Feel free to modify and adapt for your specific teaching needs.
