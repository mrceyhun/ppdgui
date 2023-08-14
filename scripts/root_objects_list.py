#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : Prints the object tree (directories and plots) of a ROOT file. Useful when there is no ROOT Tree and want to see all dirs and plots.
How to use  : python .py -f foo.root [-l 100]
"""

import ROOT
import click


def get_root_obj_tree(file_name):
    """Prints all objects inside the root file with their full paths.

    Helpful if there is no ROOT Tree object, and you want to print all sub-plots and objects with their full paths.

    Args:
        file_name: returned object from ROOT.TFile.Open("foo.root")

    Returns:

    Examples:
        my_root_file = ROOT.TFile.Open("dqm.root")
        parent_obj = [p.GetName() for p in myf.GetListOfKeys()]
        print_root_objects_dfs(my_root_file, [parent_obj])
    """

    def dfs(t_file, parents, count):
        """Nested function for DFS:deep first search recursive run to find all children of objects"""
        children = []
        for parent in parents:
            _tmp_parent = t_file.Get(parent)
            if hasattr(_tmp_parent, 'GetListOfKeys'):
                for child in _tmp_parent.GetListOfKeys():
                    # Full object of the child
                    child_full_name = parent + "/" + child.GetName()
                    # Add to return list
                    tree.append(child_full_name)
                    children.append(child_full_name)
        # If there are children, run dfs for them too. Control condition.
        if children:
            count += 1
            dfs(t_file, children, count)

    # Open root file and get TFile object
    root_f = ROOT.TFile.Open(file_name, "READ")
    root_f.SaveAs()

    # Read parent objects which is mostly one
    grand_parents = [p.GetName() for p in root_f.GetListOfKeys()]

    # Initialise the return list with starting with parents
    tree = grand_parents
    # Run dfs function
    dfs(root_f, grand_parents, 0)

    root_f.Close()
    return tree


def pretty_list_print(str_list):
    """Print the list of string in a prettier way"""
    str_list = sorted(str_list)
    for s in str_list:
        print("|" + s.count("/") * "--" + s.rsplit("/", 1)[-1])


@click.command()
@click.option('-f', '--file', required=True, type=str, help='Full or relative path of a file.')
@click.option('-l', '--limit', required=False, type=int, help='Limit of lines')
def main(file, limit):
    pretty_list_print(get_root_obj_tree(file)[:limit])


if __name__ == "__main__":
    main()
