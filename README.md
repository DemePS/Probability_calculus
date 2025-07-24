# Tree class
It is a class that helps you build a probability tree, assign probability values to its edges and compute the probabilities.
At the time I developed this package, I was working on a specific problem so you might see some hardcoded values such as LPV, DTG, etc.
They correspond to the events whose probabilities I wanted to compute. So this class might not be useful as it is right now to your own problem.
I need to find a way to make it more abstract so it can be reusable for another problem. However, if you test its functionalities you can see that they are working and the values computed are correct.

This class have several methods to make your life easier :
- A **build_struture()** method that is called when you create the object and build the structure of the tree (intended to be used only once). To create a Tree object, you need to provide a name for the root node. Example :
  ```python
  T=Tree("A")
  ```
  Then follow the instruction.
- A **set_weights(list[int])** to set the weights on the edges
- A **save_struture(file_name)** to save the tree object as a binary object
- A **draw()** to method to visualize the tree
- A **compute_prob(event)** to compute the probability of an event   

# To install the dependencies

Make sure you have at least python3.10 installed on your machine then go to your working directory and follow these steps :

```bash
python3 -m venv venv #to install your virtual environment
source venv/bin/activate #to activate your virtual environment
pip install -r requirements.txt #to install the required packages
```
