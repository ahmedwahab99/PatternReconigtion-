import numpy


def MyDBSCAN(D, eps, MinPts):
    """""
    # Initially all labels are 0 when unvisited.
    #if a point was labeled -1 that means it was considered as noise
    #if it was visited and it was not considered to be noise it will be labeled with a number

    """""
    labels = [0] * len(D)

    # ID of the current cluster.
    C = 0
    for P in range(0, len(D)):  # TO Visit all points in data
        """""
         if the points label is not 0 which mean the
         point was not visited before start working

        """""

        if not (labels[P] == 0):
            continue
        """""
        To find all points in the neighbor 
        which is a circle around the point 
        """""
        neighborPts = regionQuery(D, P, eps)

        """""
        if the point haas less than minimum inits neighbor 
        consider it noise and label it woth -1
        else, start a new cluster 
        """""
        if len(neighborPts) < MinPts:
            labels[P] = -1

        else:
            C += 1
            growCluster(D, labels, P, neighborPts, C, eps, MinPts)
    return labels


def growCluster(D, labels, P, NeighborPts, C, eps, MinPts):
    """
    function to start a ne cluster

    Parameters:
      `D`      - The dataset (a list of vectors)
      `labels` - List storing the cluster labels for all dataset points
      `P`      - Index of the seed point for this new cluster
      `NeighborPts` - All of the neighbors of `P`
      `C`      - The label for this new cluster.
      `eps`    - Threshold distance
      `MinPts` - Minimum required number of neighbors
    """

    # Assign the cluster label to the seed point.
    labels[P] = C

    # Look at each neighbor of P (neighbors are referred to as Pn).
    # NeighborPts will be used as a FIFO queue of points to search--that is, it
    # will grow as we discover new branch points for the cluster. The FIFO
    # behavior is accomplished by using a while-loop rather than a for-loop.
    # In NeighborPts, the points are represented by their index in the original
    # dataset.
    i = 0
    while i < len(NeighborPts):

        # Get the next point from the queue.
        Pn = NeighborPts[i]

        # If Pn was labelled NOISE during the seed search, then we
        # know it's not a branch point (it doesn't have enough neighbors), so
        # make it a leaf point of cluster C and move on.
        if labels[Pn] == -1:
            labels[Pn] = C

        # Otherwise, if Pn isn't already claimed, claim it as part of C.
        elif labels[Pn] == 0:
            # Add Pn to cluster C (Assign cluster label C).
            labels[Pn] = C

            # Find all the neighbors of Pn
            PnNeighborPts = regionQuery(D, Pn, eps)

            # If Pn has at least MinPts neighbors, it's a branch point!
            # Add all of its neighbors to the FIFO queue to be searched.
            if len(PnNeighborPts) >= MinPts:
                NeighborPts = NeighborPts + PnNeighborPts
            # If Pn *doesn't* have enough neighbors, then it's a leaf point.
            # Don't queue up it's neighbors as expansion points.
            # else:
            # Do nothing
            # NeighborPts = NeighborPts

        # Advance to the next point in the FIFO queue.
        i += 1

        # We've finished growing cluster C!


def regionQuery(D, P, eps):
    """
     function for searching for all points in a point's neighborhood
     returns a list with labels of all points in the region
    """
    neighbors = []

    # For each point in the dataset...
    for Pn in range(0, len(D)):

        # S If the distance is below the threshold, add it to the neighbors list.
        if numpy.linalg.norm(D[P] - D[Pn]) < eps:
            neighbors.append(Pn)

    return neighbors