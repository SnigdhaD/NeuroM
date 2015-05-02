'''Basic functions used for tree analysis'''
from neurom.core import tree as tr
from neurom.analysis.morphmath import point_dist
from neurom.core.point import as_point
from neurom.core.dataformat import COLS
import numpy as np


def get_segment_lengths(tree):
    ''' return a list of segments length inside tree
    '''
    return [point_dist(as_point(s[0]), as_point(s[1]))
            for s in tr.iter_segment(tree)]


def get_segment_diameters(tree):
    ''' return a list of segments diameter inside tree
    '''
    return [as_point(s[0]).r + as_point(s[1]).r for s in tr.iter_segment(tree)]


def get_segment_radial_dists(pos, tree):
    '''Return a list of radial distances of tree segments to a given point

    Thr radial distance is the euclidian distance between the mid-point of
    the segment and the point in question.

    Args:
        pos: origin to which disrances are measured. It must have at lease 3
        components. The first 3 components are (x, y, z).

        tree: tree of raw data rows.

    '''
    return [point_dist(pos, np.divide(np.add(as_point(s[0]),
                                             as_point(s[1])), 2.0))
            for s in tr.iter_segment(tree)]


def get_segment_path_distance(tree):
    '''Get the path distance from a sub-tree to the root node'''
    return np.sum(point_dist(as_point(s[0]), as_point(s[1]))
                  for s in tr.iter_segment(tree, tr.iter_upstream))


def find_tree_type(tree):

    """
    Calculates the 'mean' type of the tree.
    Accepted tree types are:
    'undefined', 'axon', 'basal', 'apical'
    The 'mean' tree type is defined as the type
    that is shared between at least 51% of the tree's points.
    Returns a tree with a tree.type defined.
    """

    tree_types = ['undefined', 'soma', 'axon', 'basal', 'apical']

    types = [node.value[COLS.TYPE] for node in tr.iter_preorder(tree)]

    tree.type = tree_types[int(np.median(types))]

    return tree


def get_tree_type(tree):

    """
    If tree does not have a tree type,
    calculates the tree type and returns it.
    If tree has a tree type returns its precomputed type.
    """

    if not hasattr(tree, 'type'):
        tree = find_tree_type(tree)

    return tree.type