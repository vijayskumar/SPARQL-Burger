"""
SPARQL Burger - A Python SPARQL query builder for programmatically generating SPARQL graph patterns and queries.
Version 0.1
Official webpage: http://pmitzias.com/SPARQLBurger
Documentation: http://pmitzias.com/SPARQLBurger/docs.html
Created by Panos Mitzias (http://www.pmitzias.com)
Powered by Catalink Ltd (http://catalink.eu)
"""

"""
#   SPARQLSyntaxTerms.py edited by GE Research 05/20/2022, Copyright 2022 © General Electric Company, All Rights Reserved.

#   The contents of this file represent a modified version of the original file: https://github.com/panmitz/SPARQL-Burger/blob/master/SPARQLBurger/SPARQLQueryBuilder.py.
#   This research is based upon work supported in part by the Office of the Director of National Intelligence (ODNI),
#   Intelligence Advanced Research Projects Activity (IARPA), via Contract # 2021-21022600004 (GER Proposal #20-378 (258732)).
#   The views and conclusions contained herein are those of the authors and should not be interpreted as necessarily
#   representing the official policies, either expressed or implied, of ODNI, IARPA, or the U.S. Government.
#   The U.S. Government is authorized to reproduce and distribute reprints for governmental purposes notwithstanding any
#   copyright annotation therein.
"""

from SPARQLBurger.SPARQLSyntaxTerms import *


class SPARQLGraphPattern:
    def __init__(self, optional=False, union=False):
        """
        The SPARQLGraphPattern class constructor.
        :param optional: <bool> Indicates if graph pattern should be marked as OPTIONAL.
        :param union: <bool> Indicates if graph pattern should have a UNION clause that associates it with the previous.
        graph pattern
        """
        self.is_optional = optional
        self.is_union = union
        self.graph = []
        self.filters = []
        self.bindings = []
        # MODIFICATION: The following member variable 'self.havings' was added by GE Research as part of the ProCure project
        self.havings = []

    def add_triples(self, triples):
        """
        Adds a list of triples to the graph pattern.
        :param triples: <list> A list of SPARQLSyntaxTerms.Triple objects.
        :return: <bool> True if addition succeeded, False if given argument was not a list of Triple objects.
        """
        if type(triples) is list and all(isinstance(element, Triple) for element in triples):
            self.graph.extend(triples)
            return True
        else:
            return False

    def add_nested_graph_pattern(self, graph_pattern):
        """
        Adds another graph pattern as nested to the main graph pattern.
        :param graph_pattern: <obj> The SPARQLGraphPattern object to be nested.
        :return: <bool> True if addition succeeded, False if given argument was not a SPARQLGraphPattern object.
        """
        if type(graph_pattern) is SPARQLGraphPattern:
            self.graph.append(graph_pattern)
            return True
        else:
            return False

    def add_nested_select_query(self, select_query):
        """
        Adds a select query as nested to the main graph pattern.
        :param select_query: <obj> The SPARQLSelectQuery object to be nested.
        :return: <bool> True if addition succeeded, False if given argument was not a SPARQLGraphPattern object.
        """
        if type(select_query) is SPARQLSelectQuery:
            self.graph.append(select_query)
            return True
        else:
            return False

    def add_filter(self, filter):
        """
        Adds a FILTER expression to the graph pattern.
        :param filter: <obj> The Filter to be added.
        :return: <bool> True if addition succeeded, False if given argument was not a Filter object.
        """
        if type(filter) is Filter:
            self.filters.append(filter)
            return True
        else:
            return False

    # MODIFICATION: The following method 'add_having' was added by GE Research as part of the ProCure project
    def add_having(self, having):
        """
        Adds a HAVING expression to the graph pattern.
        :param filter: <obj> The HAVING expression to be added.
        :return: <bool> True if addition succeeded, False if given argument was not a Having object.
        """
        if type(having) is Having:
            self.havings.append(having)
            return True
        else:
            return False

    def add_binding(self, binding):
        """
        Adds a BIND expression to the graph pattern.
        :param binding: <obj> The Binding object to be added.
        :return: <bool> True if addition succeeded, False if given argument was not a Binding object.
        """
        if type(binding) is Binding:
            self.bindings.append(binding)
            return True
        else:
            return False

    def get_text(self, indentation_depth=0):
        """
        Generates the text for the SPARQL graph pattern.
        :param indentation_depth: <int> A value that facilitates the appropriate addition of indents to the text. Defaults at 0.
        :return: <str> The SPARQL graph pattern text. Returns empty string if an exception was raised.
        """
        try:
            # Calculate indentations
            outer_indentation = indentation_depth * "   "
            inner_indentation = (indentation_depth + 1) * "   "

            # Initialize string
            if self.is_optional:
                query_text = "%sOPTIONAL {\n" % (outer_indentation, )
            elif self.is_union:
                query_text = "%sUNION\n%s{\n" % (outer_indentation, outer_indentation)
            else:
                query_text = "%s{\n" % (outer_indentation, )

            # Add triples
            for entry in self.graph:
                # If entry is a Triple object
                if type(entry) is Triple:
                    query_text += "%s%s" % (inner_indentation, entry.get_text())

                # If entry is a nested SPARQLGraphPattern object
                elif type(entry) is SPARQLGraphPattern:

                    # Get text for nested graph pattern
                    nested_graph_text = entry.get_text(indentation_depth=indentation_depth + 1)

                    # Append nested text to graph text
                    if nested_graph_text:
                        query_text += nested_graph_text
                    else:
                        return False

                # If entry is a nested SPARQLSelectQuery object
                elif type(entry) is SPARQLSelectQuery:

                    # Get the text for the nested select query
                    nested_select_text = entry.get_text(indentation_depth=indentation_depth + 2)

                    # Append nested text to graph text
                    if nested_select_text:
                        query_text += "%s{%s%s}\n" % (inner_indentation, nested_select_text, inner_indentation)
                    else:
                        return False

            # Add binding texts
            for binding in self.bindings:
                query_text += "%s%s\n" % (inner_indentation, binding.get_text())

            # Add filter texts
            for filter in self.filters:
                query_text += "%s%s\n" % (inner_indentation, filter.get_text())

            # Finalize graph text
            query_text += "%s}\n" % (outer_indentation, )

            return query_text

        except Exception as e:
            print("Error 1 @ SPARQLGraphPattern.get_text()", e)
            return ""


class SPARQLQuery:
    def __init__(self, include_popular_prefixes=False):
        """
        The SPARQLQuery class constructor.
        :param include_popular_prefixes: <bool> If True, a list of popular namespaces will be added automatically
        """
        self.prefixes = []
        self.where = None

        if include_popular_prefixes:
            self.add_popular_prefixes()

    def add_prefix(self, prefix):
        """
        Adds a PREFIX expression to the graph pattern.
        :param prefix: <obj> The Prefix object to be added.
        :return: <bool> True if addition succeeded, False if given argument was not a Prefix object.
        """
        if type(prefix) is Prefix:
            self.prefixes.append(prefix)
            return True
        else:
            return False

    def add_popular_prefixes(self):
        popular_prefixes = {
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "xml": "http://www.w3.org/2001/XMLSchema#",
            "owl": "http://www.w3.org/2002/07/owl#",
            "prov": "http://www.w3.org/ns/prov#",
            "foaf": "http://xmlns.com/foaf/0.1/"
        }

        for prefix in popular_prefixes:
            self.add_prefix(
                prefix=Prefix(
                    prefix=prefix,
                    namespace=popular_prefixes[prefix]
                )
            )

    def set_where_pattern(self, graph_pattern):
        """
        Sets the SPARQLGraphPattern object to be used at the WHERE part
        :param graph_pattern: <obj> The SPARQLGraphPattern object to be used.
        :return: <bool> True if setting succeeded, False if given argument was not a SPARQLGraphPattern object.
        """
        if type(graph_pattern) is SPARQLGraphPattern:
            self.where = graph_pattern
            return True
        else:
            return False


class SPARQLSelectQuery(SPARQLQuery):
    def __init__(self, distinct=False, limit=False, include_popular_prefixes=False):
        """
        The SPARQLSelectQuery class constructor.
        :param distinct: <bool> Indicates if the select should be SELECT DISTINCT.
        :param limit: <int> A limit to be used for the select query results.
        """
        SPARQLQuery.__init__(self, include_popular_prefixes)

        self.distinct = distinct
        self.limit = limit
        self.variables = []
        self.group_by = []
        self.having = []
        self.order_by = []

    def add_variables(self, variables):
        """
        Adds a list of variables to be selected by the select query
        :param variables: <list> A list of variables as strings.
        :return: <bool> True if addition succeeded, False if given argument was not a list of strings.
        """
        if type(variables) is list and all(isinstance(element, str) for element in variables):
            self.variables.extend(variables)
            return True
        else:
            return False

    def add_group_by(self, group):
        """
        Adds a GROUP BY expression to the query
        :param group: <obj> The GroupBy object to be added
        :return: <bool> True if addition succeeded, False if given argument was not a GroupBy object.
        """
        if type(group) is GroupBy:
            self.group_by.append(group)
            return True
        else:
            return False

    # MODIFICATION: The following method 'add_order_by' was added by GE Research as part of the ProCure project
    def add_order_by(self, order):
        """
        Adds a ORDER BY expression to the query
        :param group: <obj> The OrderBy object to be added
        :return: <bool> True if addition succeeded, False if given argument was not a OrderBy object.
        """
        if type(order) is OrderBy:
            self.order_by.append(order)
            return True
        else:
            return False

    # MODIFICATION: The following method 'add_having' was added by GE Research as part of the ProCure project
    def add_having(self, having):
        self.having.append(having)
        return True

    def get_text(self, indentation_depth=0):
        """
        Generates the text for the SPARQL select query.
        :param indentation_depth: <int> A value that facilitates the appropriate addition of indents to the text. Defaults at 0.
        :return: <str> The SPARQL Select query text. Returns empty string if an exception was raised.
        """
        try:
            # Calculate indentation
            outer_indentation = indentation_depth * "   "

            # Initialize text string
            query_text = ""

            # Add prefixes
            for prefix in self.prefixes:
                query_text += prefix.get_text()

            # Add SELECT token
            if self.distinct:
                distinct_token = "DISTINCT "
            else:
                distinct_token = ""
            query_text += "\n%sSELECT %s" % (outer_indentation, distinct_token)

            # If some variables have been defined, add them
            if self.variables:
                query_text += " ".join(self.variables)

            # If no variable has been defined, use *
            else:
                query_text += " *"

            # Add WHERE token
            query_text += "\n%sWHERE " % (outer_indentation, )

            # Add WHERE pattern graph
            if self.where is not None:
                query_text += self.where.get_text(indentation_depth=indentation_depth)[:-1]

            # Add group by expressions
            for group in self.group_by:
                query_text += "\n%s%s" % (outer_indentation, group.get_text())

            # MODIFICATION: The following for loop statement block was added by GE Research as part of the ProCure project
            # Add having expressions
            for have in self.having:
                query_text += "\n%s%s" % (outer_indentation, have.get_text())

            # MODIFICATION: The following for loop statement block was added by GE Research as part of the ProCure project
            # Add order by expressions
            for order in self.order_by:
                query_text += "\n%s%s" % (outer_indentation, order.get_text())

            # Add limit if required
            if self.limit:
                query_text += "\nLIMIT %s" % (str(self.limit))

            return query_text

        except Exception as e:
            print("Error 1 @ SPARQLSelectQuery.get_text()", e)
            return ""


class SPARQLUpdateQuery(SPARQLQuery):
    def __init__(self, include_popular_prefixes=False):
        """
        The SPARQLUpdateQuery class constructor.
        """
        SPARQLQuery.__init__(self, include_popular_prefixes)
        self.delete = None
        self.insert = None

    def set_delete_pattern(self, graph_pattern):
        """
        Sets the SPARQLGraphPattern object to be used at the DELETE part
        :param graph_pattern: <obj> The SPARQLGraphPattern object to be used.
        :return: <bool> True if setting succeeded, False if given argument was not a SPARQLGraphPattern object.
        """
        if type(graph_pattern) is SPARQLGraphPattern:
            self.delete = graph_pattern
            return True
        else:
            return False

    def set_insert_pattern(self, graph_pattern):
        """
        Sets the SPARQLGraphPattern object to be used at the INSERT part.
        :param graph_pattern: <obj> The SPARQLGraphPattern object to be used.
        :return: <bool> True if setting succeeded, False if given argument was not a SPARQLGraphPattern object.
        """
        if type(graph_pattern) is SPARQLGraphPattern:
            self.insert = graph_pattern
            return True
        else:
            return False

    def get_text(self, indentation_depth=0):
        """
        Generates the text for the SPARQL update query.
        :param indentation_depth: <int> A value that facilitates the appropriate addition of indents to the text. Defaults at 0.
        :return: <str> The SPARQL Update query text. Returns empty string if an exception was raised.
        """

        try:
            # Calculate indentation
            outer_indentation = indentation_depth * "   "

            # Initialize text string
            query_text = ""

            # Add prefixes
            for prefix in self.prefixes:
                query_text += prefix.get_text()

            # If a delete graph pattern has been defined
            if self.delete is not None:

                # Add DELETE token
                query_text += "\n%sDELETE " % (outer_indentation,)

                # Add DELETE pattern graph
                query_text += self.delete.get_text(indentation_depth=indentation_depth)[:-1]

            # If an insert graph pattern has been defined
            if self.insert is not None:
                # Add INSERT token
                query_text += "\n%sINSERT " % (outer_indentation,)

                # Add INSERT pattern graph
                query_text += self.insert.get_text(indentation_depth=indentation_depth)[:-1]

            # If a where graph pattern has been defined
            if self.where is not None:
                # Add WHERE token
                query_text += "\n%sWHERE " % (outer_indentation,)

                # Add WHERE pattern graph
                query_text += self.where.get_text(indentation_depth=indentation_depth)[:-1]

            return query_text

        except Exception as e:
            print("Error 1 @ SPARQLUpdateQuery.get_text()", e)
            return ""


if __name__ == "__main__":

    # Create a graph pattern
    pattern = SPARQLGraphPattern()

    # Add a triple
    pattern.add_triples(
        triples=[
            Triple(subject="?person", predicate="rdf:type", object="ex:Person"),
            Triple(subject="?person", predicate="ex:hasName", object="?name")
        ]
    )

    # Create a second graph pattern that should be OPTIONAL
    optional_pattern = SPARQLGraphPattern(optional=True)

    # Add a triple to the optional graph pattern
    optional_pattern.add_triples(
        triples=[
            Triple(subject="?person", predicate="ex:hasAge", object="?age")
        ]
    )

    # Add optional graph pattern as nested to the main graph pattern
    pattern.add_nested_graph_pattern(optional_pattern)

    print(pattern.get_text())

    # Add some binding (BIND clause) to the main pattern.
    pattern.add_binding(
        binding=Binding(
            value="\'John\'@en",
            variable="?name"
        )
    )

    # Add another binding where we will use a nested IF clause with a BOUND clause
    pattern.add_binding(
        binding=Binding(
            value=IfClause(
                condition=Bound(
                    variable="?age"
                ),
                true_value="?age",
                false_value="32"
            ),
            variable="?years"
        )
    )

    # Add a filter for the age to the optional pattern
    optional_pattern.add_filter(
        filter=Filter(
            expression="?age > 30"
        )
    )

    # Print the graph query text
    # print(pattern.get_text())

    # Create a select query
    select_query = SPARQLSelectQuery(
        distinct=True,
        limit=1000
    )

    # Add prefix "ex"
    select_query.add_prefix(
        prefix=Prefix(
            prefix="ex",
            namespace="http://www.example.com#"
        )
    )

    # Add the variables for the selection
    select_query.add_variables("?person")
    select_query.add_variables("?years")

    # Set the graph pattern that we created earlier as the WHERE pattern
    select_query.set_where_pattern(graph_pattern=pattern)

    # Add a GROUP BY to query
    select_query.add_group_by(
        group=GroupBy(
            variables=["?person", "?age"]
        )
    )

    # # Create another graph pattern
    # pattern_3 = SPARQLGraphPattern()
    # pattern_3.add_triple(
    #     triple=Triple(
    #         subject="?person",
    #         predicate="rdf:type",
    #         object="ex:Customer"
    #     )
    # )
    #
    # # Create a new select query to be nested in the first select query
    # nested_select_query = SPARQLSelectQuery()
    # nested_select_query.add_variable("?person")
    # nested_select_query.set_where_pattern(
    #     graph_pattern=pattern_3
    # )
    #
    # # Set the second query as nested to the first graph pattern
    # pattern.add_nested_select_query(
    #     select_query=nested_select_query
    # )

    # Print the query text
    # print(select_query.get_text())

    #########################################
    # delete_pattern = SPARQLGraphPattern()
    # delete_pattern.add_triple(
    #     Triple(
    #         subject="?person",
    #         predicate="ex:hasAge",
    #         object="?age"
    #     )
    # )
    #
    # insert_pattern = SPARQLGraphPattern()
    # insert_pattern.add_triple(
    #     Triple(
    #         subject="?person",
    #         predicate="ex:hasAge",
    #         object="32"
    #     )
    # )
    #
    # where_pattern = SPARQLGraphPattern()
    # where_pattern.add_triple(
    #     Triple(
    #         subject="?person",
    #         predicate="ex:hasAge",
    #         object="?age"
    #     )
    # )
    # where_pattern.add_triple(
    #     Triple(
    #         subject="?person",
    #         predicate="ex:name",
    #         object="John"
    #     )
    # )
    #
    # # Create an update query
    # update_query = SPARQLUpdateQuery()
    # update_query.add_prefix(
    #     Prefix(
    #         prefix="ex",
    #         namespace="http://www.example.com#"
    #     )
    # )
    # update_query.set_delete_pattern(graph_pattern=delete_pattern)
    # update_query.set_insert_pattern(graph_pattern=insert_pattern)
    # update_query.set_where_pattern(graph_pattern=insert_pattern)
    #
    # print(update_query.get_text())


