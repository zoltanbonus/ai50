import csv
import sys

from degrees import load_data, shortest_path, person_id_for_name
from util import Node, StackFrontier, QueueFrontier


def main():
    load_data("small")
    try:
        test_shortest_path("Kevin Bacon", "Kevin Bacon", 1)
        test_shortest_path("Kevin Bacon", "Tom Cruise", 1)
        test_shortest_path("Kevin Bacon", "Cary Elwes", 3)
    except Exception as e:
        print("Test failed. " + str(e))


def test_shortest_path(sourceName, targetName, expectedPathLength):
    print(
        f"Executing test: sourceName: {sourceName}, targetName: {targetName}, expectedPathLength: {expectedPathLength}")
    source = person_id_for_name(sourceName)
    target = person_id_for_name(targetName)

    path = shortest_path(source, target)
    if len(path) != expectedPathLength:
        raise Exception(
            f"Invalid path length. Expected {expectedPathLength}, Actual: {len(path)}")
    else:
        print("Test passed!")


if __name__ == "__main__":
    main()
