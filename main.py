def print_tree(node):
    print(node.name)

    if node.children == []:
        return
    
    for child in node.children:
        print_tree(child)


productions = {
    "formula": [["(", "formula", "/", "\\", "formula", ")"],
                      ["disjunction"]],

    "disjunction": [["(", "disjunction", "\\", "/", "disjunction", ")"],
                      ["term"]],

    "term": [["var"], ["negation"]],

    "negation": [["(", "!", "var", ")"]],

    "var": [["letter"]],

    "letter": [[chr(i)] for i in range(ord("A"), ord("Z") + 1)]
}

nonterminals = list(productions.keys())
terminals = list([symbol for productions in productions.values() for production in productions for symbol in production if symbol not in nonterminals])


def get_productions(value):
    return productions[value]


def is_terminal(value):
    return value in terminals


def is_nonterminal(value):
    return value in nonterminals


class TreeNode:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []


    def add_child(self, node):
        self.children.append(node)

    
    def get_rightmost(self):
        return self.children[-1]
    

    def get_leftmost(self):
        return self.children[0]
    

    def get_leftmost_nonterminal(self):
        return list(filter(lambda x: is_nonterminal(x.name), self.children))[0]
    

    def get_rightmost_nonterminal(self):
            return list(filter(lambda x: is_nonterminal(x.name), self.children))[-1]
    

    def __repr__(self):
        return f"{self.name}: {self.children}"
    

def get_all_disjuncts(node: TreeNode):
    def handle_disjunct(node: TreeNode):
        def handle_term(node: TreeNode):
            def handle_var(node: TreeNode):
                if node == False:
                    return False

                result = node.get_rightmost().get_leftmost().name

                return result

            print(node)

            result = "";

            subterm = node.get_leftmost_nonterminal();
            var_nt = None;

            if subterm.name == "negation":
                result += "not ";
                var_nt = subterm.get_leftmost_nonterminal();

            else:
                var_nt = subterm;

            result += handle_var(var_nt);

            return result;

        print(node)

        if node == False:
            return False

        elif len(node.children) == 1:
            return [handle_term(node.get_leftmost_nonterminal())];

        result = [];

        result.extend(handle_disjunct(node.get_leftmost_nonterminal()));
        result.extend(handle_disjunct(node.get_rightmost_nonterminal()));

        return result;

    print(node)

    if node == False:
        return False

    elif len(node.children) == 1:
        return [handle_disjunct(node.get_leftmost_nonterminal())];

    terms = [];

    terms.extend(get_all_disjuncts(node.get_leftmost_nonterminal()));
    terms.extend(get_all_disjuncts(node.get_rightmost_nonterminal()));

    return terms;


def get_parse_tree(text):
    def recursive_descent(symbol):
        nonlocal text

        if is_terminal(symbol) and text[0] != symbol:
            return False
        
        elif symbol is None:
            return TreeNode(symbol)
        
        elif is_terminal(symbol) and text[0] == symbol:
            text = text[1:]
            return TreeNode(symbol)
        
        elif not is_nonterminal(symbol):
            return False
        
        current_text = text
        productions = get_productions(symbol)

        current_node = TreeNode(symbol)

        for prod in productions:
            result = False
            nodes = []

            for char in prod:
                result = recursive_descent(char)

                if result == False:
                    text = current_text
                    break

                nodes.append(result)

            if result != False:
                # nodes.reverse()

                for child in nodes:
                    current_node.add_child(child)

                return current_node
            
        return False
    
    if text == "":
        return False
    
    tree = recursive_descent("formula")
    
    return tree


def get_letter(var):
    parts = var.split(' ')

    if parts[0] == 'not':
        return parts[1]
    
    return parts[0]


def has_duplicates(disjunct):
    letters = []

    for var in disjunct:
        letter = get_letter(var)

        if letter in letters:
            return True
        
        letters.append(letter)
        
    return False


def is_ccnf(disjuncts):
    if disjuncts == False:
        return False
    
    vars = set()
    visited = []

    for disjunct in disjuncts:
        for var in disjunct:
            vars.add(get_letter(var))

        if (has_duplicates(disjunct)):
            return False

        if visited == []:
            visited.append(disjunct)

        elif disjunct in visited:
            return False
                
    for disjunct in disjuncts:
        for var in vars:
            if var not in disjunct and "not " + var not in disjunct:
                return False
    
    return True


# // На основе списка коньюнкций определяет,
# // является ли формула СДНФ
# const isCDNF = (terms) => {
#     if (terms == undefined || terms == null || terms == false || terms.length == 0)
#         return false;

#     let variables = [];

#     for (let i = 0; i < terms.length - 1; i ++) {
#         for (let j = i + 1; j < terms.length; j ++) {
#             fst_term = terms[i];
#             snd_term = terms[j];

#             if (fst_term.length != snd_term.length)
#                 return false;

#             let duplicates = new Map();

#             for (const variable of fst_term) {
#                 let var_name = variable.split(" ");

#                 if (var_name.length == 1)
#                     var_name = var_name[0];

#                 else
#                     var_name = var_name[1];

#                 if (duplicates.get(var_name) == undefined)
#                     duplicates.set(var_name, 1);

#                 else
#                     return false;
#             }

#             duplicates = new Map();

#             for (const variable of snd_term) {
#                 let var_name = variable.split(" ");

#                 if (var_name.length == 1)
#                     var_name = var_name[0];

#                 else
#                     var_name = var_name[1];

#                 if (duplicates.get(var_name) == undefined)
#                     duplicates.set(var_name, 1);

#                 else
#                     return false;
#             }   

#             let is_all_equal = true;

#             for (const variable of fst_term)
#                 is_all_equal &&= snd_term.includes(variable);

#             if (is_all_equal) 
#                 return false;

#             for (let i = 0; i < fst_term.length; i ++) {
#                 let fst_var_name = fst_term[i].split(" ");

#                 if (fst_var_name.length == 1)
#                     fst_var_name = fst_var_name[0];

#                 else
#                     fst_var_name = fst_var_name[1];

#                 if (! variables.includes(fst_var_name))
#                     variables.push(fst_var_name);

#                 let snd_var_name = snd_term[i].split(" ");

#                 if (snd_var_name.length == 1)
#                     snd_var_name = snd_var_name[0];

#                 else
#                     snd_var_name = snd_var_name[1];

#                 if (! variables.includes(snd_var_name))
#                     variables.push(snd_var_name);
#             }
#         }
#     }

#     if (terms.length == 1) {
#         let duplicates = new Map();

#         term = terms[0];

#         for (const variable of term) {
#             let var_name = variable.split(" ");

#             if (var_name.length == 1)
#                 var_name = var_name[0];

#             else
#                 var_name = var_name[1];

#             if (duplicates.get(var_name) == undefined)
#                 duplicates.set(var_name, 1);

#             else
#                 return false;
#         }
#     }

#     if (variables.length != terms[0].length && terms.length != 1)
#         return false;

#     return true;
# }

if __name__ == "__main__":
    text = input()

    parse_tree = get_parse_tree(text)
    # print(print_tree(parse_tree))

    # print(parse_tree)
    conjuncts = get_all_disjuncts(parse_tree)

    print(conjuncts)
    answer = is_ccnf(conjuncts)

    print(answer)
