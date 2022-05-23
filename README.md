# SPARQL Burger

SPARQL Burger is a **Python SPARQL query builder** that automates the generation of SPARQL graph patterns, SPARQL Select and SPARQL Update queries. Just like stacking onions, tomatos and cheese to assemble the right burger, SPARQL Burger offers the necessary ingredients for the assembly of meaningful SPARQL queries in an OOP manner.

_This [repository](https://github.com/vijayskumar/SPARQL-Burger) is a "Derivative Work" that is based on an original [repository](https://github.com/panmitz/SPARQL-Burger), wherein a number of modifications have been made by us (GE Research) to the files in "Source" form, as per definitions in the W3C SOFTWARE NOTICE AND LICENSE listed [here](https://github.com/panmitz/SPARQL-Burger/blob/master/LICENSE.txt). These modifications were carried out as a part of work supported by the Office of the Director of National Intelligence (ODNI), Intelligence Advanced Research Projects Activity (IARPA), via Contract # 2021-21022600004 (Proposal # GER Proposal #20-378 (258732))._

The following files from the original repository have been modified within this redistributed version:

 - [README.md](README.md)
 - [SPARQLBurger/SPARQLQueryBuilder.py](SPARQLBurger/SPARQLQueryBuilder.py)
 - [SPARQLBurger/SPARQLSyntaxTerms.py](SPARQLBurger/SPARQLSyntaxTerms.py)

The date of modification of the above files was May 20th, 2022.
Where applicable, the specifics of the modifications have been described or highlighted using comments within the respective files.

The following new files have been added as part of this redistributed version:
 
 - [setup.py](setup.py) - code to package and install SPARQLBurger as a module within some Python environment
 - [requirements.txt](requirements.txt) - requirements file for pip install of SPARQLBurger as a packaged module
 - [SPARQLBurger/__init__.py](SPARQLBurger/__init__.py) - empty init file for package installation purposes

## Getting Started
SPARQL Burger is a minimal module for Python (2.x and 3.x).

### Prerequisites

- Python (2.x or 3.x)

### Installation

* #### Manually
 
 1. First, install the dependency packages within your Python environment: ```pip install -r requirements.txt```
 2. Create and install SPARQLBurger wheel file:
```
python setup.py sdist bdist_wheel                                 # create wheel file
pip install <MY_PATH>/dist/SPARQLBurger-0.0.1-py3-none-any.whl    # install wheel file
```

## Usage examples
### 1. Create a SPARQL graph pattern and add some triples
In this example we generate a minimal [SPARQL graph pattern](http://https://www.w3.org/TR/rdf-sparql-query/#GraphPattern "SPARQL graph pattern"). A graph pattern, delimited with `{ }`, is a building block for SPARQL queries and more than one can be nested and/or united to form a more complex graph pattern.

<details>
 <summary>Show example</summary>

```python
from SPARQLBurger.SPARQLQueryBuilder import *

# Create a graph pattern
pattern = SPARQLGraphPattern()

# Add a couple of triples to the pattern
pattern.add_triples(
        triples=[
            Triple(subject="?person", predicate="rdf:type", object="ex:Person"),
            Triple(subject="?person", predicate="ex:hasName", object="?name")
        ]
    )

# Let's print this graph pattern
print(pattern.get_text())
```
The printout is:
```
{
   ?person rdf:type ex:Person . 
   ?person ex:hasName ?name . 
}
```
</details>

### 2. Create an OPTIONAL pattern and nest it to the main pattern
Here, the main graph pattern contains another graph pattern that is declared as OPTIONAL. In general, graph patterns can contain as many nesting levels as necessary. Nesting a pattern to itself, though, would result to an error.

<details>
 <summary>Show example</summary>

```python
from SPARQLBurger.SPARQLQueryBuilder import *

# Create a main graph pattern and add some triples
main_pattern = SPARQLGraphPattern()
main_pattern.add_triples(
        triples=[
            Triple(subject="?person", predicate="rdf:type", object="ex:Person"),
            Triple(subject="?person", predicate="ex:hasName", object="?name")
        ]
    )

# Create an optional pattern and add a triple
optional_pattern = SPARQLGraphPattern(optional=True)
optional_pattern.add_triples(
        triples=[
            Triple(subject="?person", predicate="ex:hasAge", object="?age")
        ]
    )

# Nest the optional pattern to the main
main_pattern.add_nested_graph_pattern(optional_pattern)

# Let's print the main graph pattern
print(pattern.get_text())
```
The printout is:
```
{
   ?person rdf:type ex:Person . 
   ?person ex:hasName ?name . 
   OPTIONAL {
      ?person ex:hasAge ?age . 
   }
}
```
</details>

### 3. Create a UNION of graph patterns
In this example we will declare a main graph pattern that contains two other graph patterns associated with UNION.

<details>
 <summary>Show example</summary>

```python
from SPARQLBurger.SPARQLQueryBuilder import *

# Create an empty graph pattern
main_pattern = SPARQLGraphPattern()

# Create the first graph pattern to be nested and add some triples
first_pattern = SPARQLGraphPattern()
first_pattern.add_triples(
        triples=[
            Triple(subject="?person", predicate="rdf:type", object="ex:Person"),
            Triple(subject="?person", predicate="ex:hasName", object="?name")
        ]
    )

# Create the second graph pattern to be nested as a UNION to the first and add some triples
second_pattern = SPARQLGraphPattern(union=True)
second_pattern.add_triples(
        triples=[
            Triple(subject="?person", predicate="rdf:type", object="ex:User"),
            Triple(subject="?person", predicate="ex:hasNickname", object="?name")
        ]
    )

# Nest both patterns to the main one
main_pattern.add_nested_graph_pattern(graph_pattern=first_pattern)
main_pattern.add_nested_graph_pattern(graph_pattern=second_pattern)

# Let's print the main graph pattern
print(main_pattern.get_text())
```
The printout is:
```
{
   {
      ?person rdf:type ex:Person . 
      ?person ex:hasName ?name . 
   }
   UNION
   {
      ?person rdf:type ex:User . 
      ?person ex:hasNickname ?name . 
   }
}
```
</details>

### 4. Adding FILTER, BIND and IF definitions
So far we have created simple and nested graph patterns. Now let's see how to add filters, bindings and if clauses.

<details>
 <summary>Show example</summary>

```python
from SPARQLBurger.SPARQLQueryBuilder import *

# Create a graph pattern and add some triples
pattern = SPARQLGraphPattern()
pattern.add_triples(
        triples=[
            Triple(subject="?person", predicate="rdf:type", object="ex:Person"),
            Triple(subject="?person", predicate="ex:hasAge", object="?age")
        ]
    )

# Add a filter for variable ?age
pattern.add_filter(
    filter= Filter(
        expression="?age < 65"
    )
)

# Add a binding for variable ?years_alive
pattern.add_binding(
    binding=Binding(
        value="?age",
        variable="?years_alive"
    )
)

# Add a binding for variable ?status, that should be "minor" or "adult" based on the ?age value
pattern.add_binding(
    binding=Binding(
        value=IfClause(
            condition="?age >= 18",
            true_value="'adult'",
            false_value="'minor'"
        ),
        variable="?status"
    )
)

# Print the graph pattern
print(pattern.get_text())
```
The printout is:
```
{
   ?person rdf:type ex:Person . 
   ?person ex:hasAge ?age . 
   BIND (?age AS ?years_alive)
   BIND (IF (?age >= 18, 'adult', 'minor') AS ?status)
   FILTER (?age < 65)
}
```
In the first BIND we have only provided a value and a variable as string, but this is not always the case. In the second BIND we nested an IF clause. Therefore, the `Binding.value` also accepts objects of classes like `IfClause`. In a similar way, the arguments of `IfClause` can also be other objects of type `IfClause` and `Bound` in a nested format, as shown below. 
```python
from SPARQLBurger.SPARQLQueryBuilder import *

# Create a graph pattern and add a triple
pattern = SPARQLGraphPattern()
pattern.add_triples(
        triples=[
            Triple(subject="?person", predicate="rdf:type", object="ex:Person"),
        ]
    )

# Create an optional graph pattern and add a triple
optional_pattern = SPARQLGraphPattern(optional=True)
optional_pattern.add_triples(
        triples=[
            Triple(subject="?person", predicate="ex:hasAddress", object="?address")
        ]
    )

# Add a binding with nested a IF clause and a BOUND condition
pattern.add_binding(
    binding=Binding(
        value=IfClause(
            condition=Bound(
                variable="?address"
            ),
            true_value="?address",
            false_value="'Unknown'"
        ),
        variable="?address"
    )
)

# Print the graph pattern
print(pattern.get_text())
```
The printout is:
```
{
   ?person rdf:type ex:Person . 
   BIND (IF (BOUND (?address), ?address, 'Unknown') AS ?address)
}
```
</details>

### 5. Create a SPARQL Select query
Now that we have mastered the definition of graph patterns, let's create a simple Select query.

<details>
 <summary>Show example</summary>

```python
from SPARQLBurger.SPARQLQueryBuilder import *

# Create an object of class SPARQLSelectQuery and set the limit for the results to 100
select_query = SPARQLSelectQuery(distinct=True, limit=100)

# Add a prefix
select_query.add_prefix(
    prefix=Prefix(prefix="ex", namespace="http://www.example.com#")
)

# Add the variables we want to select
select_query.add_variables(variables=["?person", "?age"])

# Create a graph pattern to use for the WHERE part and add some triples
where_pattern = SPARQLGraphPattern()
where_pattern.add_triples(
        triples=[
            Triple(subject="?person", predicate="rdf:type", object="ex:Person"),
            Triple(subject="?person", predicate="ex:hasAge", object="?age"),
            Triple(subject="?person", predicate="ex:address", object="?address"),
        ]
    )

# Set this graph pattern to the WHERE part
select_query.set_where_pattern(graph_pattern=where_pattern)

# Group the results by age
select_query.add_group_by(
    group=GroupBy(
        variables=["?age"]
    )
)

# Print the query we have defined
print(select_query.get_text())
```
The printout is:
```
PREFIX ex: <http://www.example.com#>

SELECT DISTINCT ?person ?age
WHERE {
   ?person rdf:type ex:Person . 
   ?person ex:hasAge ?age . 
   ?person ex:address ?address . 
}
GROUP BY ?age
LIMIT 100
```
</details>

### 6. Create a SPARQL Update query
Quite similarly we can exploit graph patterns to create a SPARQL Update query (in the DELETE/INSERT form).

<details>
 <summary>Show example</summary>

```python
from SPARQLBurger.SPARQLQueryBuilder import *

# Create a SPARQLUpdateQuery object
update_query = SPARQLUpdateQuery()

# Add a prefix
update_query.add_prefix(
    prefix=Prefix(prefix="ex", namespace="http://www.example.com#")
)

# Create a graph pattern for the DELETE part and add a triple
delete_pattern = SPARQLGraphPattern()
delete_pattern.add_triples(
    triples=[
        Triple(subject="?person", predicate="ex:hasAge", object="?age")
    ]
)

# Create a graph pattern for the INSERT part and add a triple
insert_pattern = SPARQLGraphPattern()
insert_pattern.add_triples(
    triples=[
        Triple(subject="?person", predicate="ex:hasAge", object="32")
    ]
)

# Create a graph pattern for the WHERE part and add some triples
where_pattern = SPARQLGraphPattern()
where_pattern.add_triples(
    triples=[
        Triple(subject="?person", predicate="rdf:type", object="ex:Person"),
        Triple(subject="?person", predicate="ex:hasAge", object="?age")
    ]
)

# Now let's append these graph patterns to our query
update_query.set_delete_pattern(graph_pattern=delete_pattern)
update_query.set_insert_pattern(graph_pattern=insert_pattern)
update_query.set_where_pattern(graph_pattern=where_pattern)

# Print the query we have defined
print(update_query.get_text())
```
The printout is:
```
PREFIX ex: <http://www.example.com#>

DELETE {
   ?person ex:hasAge ?age . 
}
INSERT {
   ?person ex:hasAge 32 . 
}
WHERE {
   ?person rdf:type ex:Person . 
   ?person ex:hasAge ?age . 
}
```
</details>

## Documentation
[The official webpage](http://pmitzias.com/SPARQLBurger) - [The Docs](http://pmitzias.com/SPARQLBurger/docs.html)

## Authors
* [Panos Mitzias](http://pmitzias.com) - Design and development
* [Stratos Kontopoulos](http://stratoskontopoulos.com) - Contribution to the design

## Applications
SPARQL Burger has been deployed in the following projects:

* [CASPAR Framework](https://www.linkedin.com/showcase/caspar-framework)
 
## Notes

**README.md** edited by GE Research 05/20/2022, Copyright 2022 © General Electric Company, All Rights Reserved.

_The contents of this README file represent a modified version of the original file: [README.md](https://github.com/panmitz/SPARQL-Burger/README.md). This research is based upon work supported in part by the Office of the Director of National Intelligence (ODNI), Intelligence Advanced Research Projects Activity (IARPA), via Contract # 2021-21022600004 (GER Proposal #20-378 (258732)). The views and conclusions contained herein are those of the authors and should not be interpreted as necessarily representing the official policies, either expressed or implied, of ODNI, IARPA, or the U.S. Government. The U.S. Government is authorized to reproduce and distribute reprints for governmental purposes notwithstanding any copyright annotation therein._
