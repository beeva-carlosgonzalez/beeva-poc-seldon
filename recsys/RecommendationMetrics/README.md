# **Recommendation Metrics**

## **Seldon Platform**

You can test MAP@k in the seldon platform, for two algorithms, MatrixFactor and ItemSimilarity.
### Files involved:
* SeldonTests.py: Main utility to perform test
* SeldonRestAccess.py: Knows how to handle the Seldon REST API

### How to invoke it:

* Execute: _python SeldonTests.py --host={web url} 
 --consumerkey={consumerkey} 
 --consumersecret={consumersecret} 
 --algorithm={itemsimilarity|matrixfactor}_
 --compareactionsfile={filename}
 [--insertactionsfile={filename}] (This one just in case you are using similar items)

* compareactions and insertactions files should be in this folder