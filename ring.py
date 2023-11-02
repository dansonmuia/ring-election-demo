import random


class Election:
    def __init__(self, initiator):
        self.initiator = initiator
        self.candidates = [initiator]


class Node:
    coordinator = None

    def __init__(self, node_id, next_node=None):
        self.node_id = node_id
        self.name = f'Node {node_id}'
        self.next_node = next_node

    def __repr__(self):
        return self.name

    def set_coordinator(self, winner, sender):
        if sender.node_id == self.node_id:
            return
        self.coordinator = winner
        self.next_node.set_coordinator(winner, sender)

    def do_election(self, election=None):
        # Start of election
        if election is None:
            election = Election(self)
            self.next_node.do_election(election)

        # Pick election winner
        elif election.initiator.node_id == self.node_id:
            # pick election winner
            largest_node = election.candidates[0]
            for candidate in election.candidates:
                if candidate.node_id > largest_node.node_id:
                    largest_node = candidate

            # Broadcast election winner
            self.coordinator = largest_node
            self.next_node.set_coordinator(largest_node, self)

        # propagate election
        else:
            election.candidates.append(self)
            self.next_node.do_election(election)


if __name__ == '__main__':
    print('creating nodes...')
    n = 10
    nodes = []

    next_node = None

    for i in range(n):
        node = Node(i, next_node=next_node)
        next_node = node
        nodes.append(node)

    # set next node for the first node created
    nodes[0].next_node = nodes[-1]

    print('Nodes created: ')
    print(nodes)

    # Pick random node to start election
    node = nodes[random.randrange(0, n)]
    print('Randon node picked to initiate election: ', node)

    # Starting election
    print('Starting election...\n')
    node.do_election()

    print('Election results: ')
    for node in nodes:
        print(f'{node.name} has coordinator: {node.coordinator}')
