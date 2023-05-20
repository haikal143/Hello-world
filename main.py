# Muhammad Firdaus Bin Asrar            2019857
# Muhammad Darwish Bin Mohd Sukri       2014169
# Muhammad Adzim Bin Rosly              2013413

import tkinter as tk

# Infix-Postfix Calculator


class Leg:
    def __init__(self, c, x0, y0, x1, y1, x2, y2, node_p):
        self.width = 2

        c.create_line(x0 + node_p[0], y0, x1, y0, width=self.width, fill='red')
        c.create_line(x1, y0, x1, y1 - node_p[1], width=self.width, fill='red')
        c.create_line(x0 - node_p[0], y0, x2, y0, width=self.width, fill='red')
        c.create_line(x2, y0, x2, y2 - node_p[1], width=self.width, fill='red')


class Node:
    def __init__(self, c, x, y, text, text_w):
        self.width = 2
        self.tw = 10
        self.th = 10
        self.x = x
        self.y = y

        self.tw = self.tw * text_w
        c.create_rectangle(x - self.tw, y - self.th, x + self.tw, y + self.th, width=self.width)
        c.create_text(x, y, text=text)

    def get_pad(self):
        return [self.tw, self.th]

    def get_size(self):
        return [self.tw * 2, self.th * 2]


class Stack:
    def __init__(self):
        self.list = []

    def top(self):
        if self.len() == 0:
            return None
        else:
            return self.list[-1]

    def push(self, elem):
        self.list.append(elem)

    def pop(self):
        return self.list.pop()

    def len(self):
        return len(self.list)


class GStack:
    def __init__(self):
        self.stack = Stack()

        self.lbl_token = []
        self.lbl_return = []
        self.lbl_result = []

        self.sb_table = TXScrollbar(master=frm_stack_output, row=0, column=1, height=15, table_row=0)
        self.sb_table.set_button(self.table_up, self.table_down)

    def top(self):
        return self.stack.top()

    def push(self, elem):
        self.stack.push(elem)
        self.push_to_table('push(\'' + elem + '\')', '', str(self.stack.list))

    def pop(self):
        result = self.stack.pop()
        self.push_to_table('pop()', result, str(self.stack.list))
        return result

    def len(self):
        return self.stack.len()

    def init_table(self):
        self.lbl_token.append(tk.Label(master=frm_stack_table, text='Token', padx=0, relief='groove'))
        self.lbl_return.append(tk.Button(master=frm_stack_table, text='Return', padx=0, relief='groove',
                                         command=state_1))
        self.lbl_result.append(tk.Label(master=frm_stack_table, text='Result', padx=0, relief='groove'))

    def push_to_table(self, str_token, str_return, str_result):
        str1 = '\t' + str_token + '\t'
        str2 = '\t' + str_return + '\t'
        str3 = '\t' + str_result + '\t'

        self.lbl_token.append(tk.Label(master=frm_stack_table, text=str1, padx=0, relief='groove', anchor=tk.W))
        self.lbl_return.append(tk.Label(master=frm_stack_table, text=str2, padx=0, relief='groove', anchor=tk.W))
        self.lbl_result.append(tk.Label(master=frm_stack_table, text=str3, padx=0, relief='groove', anchor=tk.W))

        self.sb_table.bind(self.lbl_token[-1])
        self.sb_table.bind(self.lbl_return[-1])
        self.sb_table.bind(self.lbl_result[-1])

    def table_pack(self, row):
        self.lbl_token[0].grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S)
        self.lbl_return[0].grid(row=0, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
        self.lbl_result[0].grid(row=0, column=2, sticky=tk.W + tk.E + tk.N + tk.S)

        i = 1
        while i < 15 + 1:
            if i >= len(self.lbl_token):
                break

            self.lbl_token[row + i].grid(row=i, column=0, sticky=tk.W + tk.E)
            self.lbl_return[row + i].grid(row=i, column=1, sticky=tk.W + tk.E)
            self.lbl_result[row + i].grid(row=i, column=2, sticky=tk.W + tk.E)
            i += 1
        btn_stack_back.grid(row=1, column=0)

    def table_unpack(self):
        for i in range(len(self.lbl_token)):
            self.lbl_token[i].grid_forget()
            self.lbl_return[i].grid_forget()
            self.lbl_result[i].grid_forget()

    def table_up(self):
        self.table_unpack()
        self.table_pack(self.sb_table.tab_row)

    def table_down(self):
        self.table_unpack()
        self.table_pack(self.sb_table.tab_row)

    def delete_data(self):
        for i in range(len(self.lbl_token)):
            self.lbl_token.pop()
            self.lbl_return.pop()
            self.lbl_result.pop()

        self.stack.list.clear()

    def get_list(self):
        return self.stack.list


class TreeGenerator:
    def __init__(self):
        self.exp = []
        self.x = []
        self.y = []

        self.node = []
        self.leg = []

    def is_coord(self, x, y):
        for i in range(len(self.x)):
            if x == self.x[i] and y == self.y[i]:
                return True
        return False

    def input(self, expression):
        self.node = []
        self.leg = []
        self.exp = expression.copy()
        self.exp.reverse()
        self.y = []
        self.x = []
        exp = self.exp
        stack = Stack()

        current = 0
        self.y.append(current)
        i = 1
        while i < len(self.exp):
            prev = exp[i - 1]
            if PostfixConverter.is_operator(prev):
                current += 1
                self.y.append(current)
                if current == stack.top():
                    stack.pop()
                else:
                    stack.push(current)
            else:
                current = stack.pop()
                self.y.append(current)
            i += 1

        self.x = ([0]*len(self.y)).copy()
        current = 0

        i = 1
        while i < len(self.y):
            i1 = self.y[i]
            i2 = self.y[i-1]
            if i1 == i2:
                current = self.x[i-1] + 2
                self.x[i] = current
            elif i1 < i2:
                j = i - 1
                while j >= 0:
                    if i1 == self.y[j]:
                        current = self.x[j-1] + 1
                        break
                    j -= 1

            self.x[i] = current

            j = i
            while j > 0:
                token = self.x[j]
                k = j - 1
                while k >= 0:
                    if token == self.x[k]:
                        self.x[k] += 1
                        k -= 1
                        break
                    k -= 1
                j -= 1
            i += 1

        max_coord = max(self.x)
        for i in range(len(self.x)):
            self.x[i] = max_coord - self.x[i]

        highest = self.y[0]
        i = 1
        while i < len(self.y):
            if self.y[i] > highest:
                highest = self.y[i]
            i += 1
        size_y = 20 * (highest + 1) + 10

        highest = len(self.exp[0])
        i = 1
        while i < len(self.exp):
            if len(self.exp[i]) > highest:
                highest = len(self.exp[i])
            i += 1
        size_x = 20 * highest * len(self.exp) + 10

        cnv_tree.config(width=size_x, height=size_y)

        for i in range(len(self.exp)):
            self.node.append(Node(cnv_tree,
                                  10 + (highest * 20) / 2 + self.x[i] * 20 * highest,
                                  15 + self.y[i] * 20,
                                  self.exp[i],
                                  highest))

        i = 0
        while i < len(self.exp):
            if not PostfixConverter.is_operator(self.exp[i]):
                i += 1
                continue
            x = self.x[i] + 1
            y = self.y[i] + 1
            coord = []
            while x <= max_coord:
                if self.is_coord(x, y):
                    coord.append(10 + (highest * 20) / 2 + x * 20 * highest)
                    coord.append(15 + y * 20)
                    break
                x += 1
            x = self.x[i] - 1
            while x <= max_coord:
                if self.is_coord(x, y):
                    coord.append(10 + (highest * 20) / 2 + x * 20 * highest)
                    coord.append(15 + y * 20)
                    break
                x -= 1
            self.leg.append(Leg(cnv_tree,
                                10 + (highest * 20) / 2 + self.x[i] * 20 * highest,
                                15 + self.y[i] * 20,
                                coord[0], coord[1],
                                coord[2], coord[3],
                                self.node[0].get_pad()))
            i += 1


class TXScrollbar:
    def __init__(self, master, row, column, height, table_row=0):
        self.master = master
        self.frm = tk.Frame(master=self.master)
        self.row = row
        self.column = column
        self.height = height
        self.tab_row = table_row
        self.max_row = None
        self.up_pressed = None
        self.down_pressed = None
        btn_w = 1

        self.btn_up = tk.Button(master=self.frm, width=btn_w, relief='solid', command=lambda: self.up(1))
        self.btn_down = tk.Button(master=self.frm, width=btn_w, relief='solid', command=lambda: self.down(1))
        self.bar_w = None
        self.bar_h = None
        self.cnv_bar = None

        self.bind(self.btn_up)
        self.bind(self.btn_down)

    def bind(self, master):
        master.bind('<MouseWheel>', lambda event: self.scroll(event))

    def init_bar(self, pxl_h, max_row):
        self.bar_w = self.btn_up.winfo_reqwidth()
        self.bar_h = pxl_h * (self.height - 2)

        self.cnv_bar = tk.Canvas(master=self.frm,
                                 width=self.bar_w,
                                 height=self.bar_h,
                                 bg='gray50')

        self.bind(self.cnv_bar)

        self.max_row = max_row
        self.update_bar()

    def update_bar(self):
        self.cnv_bar.delete('all')
        self.cnv_bar.create_rectangle(3, 3, self.bar_w + 1, self.bar_h + 1, width=2)
        self.cnv_bar.create_rectangle(5,
                                      5 + (self.bar_h - 2) / self.max_row * self.tab_row,
                                      self.bar_w - 2,
                                      (self.bar_h - 2) / self.max_row * (self.height + self.tab_row),
                                      fill='#F0F0F0')

    def up(self, step):
        if self.tab_row - step >= 0:
            self.tab_row -= step
            self.up_pressed()
            self.update_bar()

    def down(self, step):
        if self.tab_row + self.height + step < self.max_row + 1:
            self.tab_row += step
            self.down_pressed()
            self.update_bar()

    def set_button(self, up_command, down_command):
        self.up_pressed = up_command
        self.down_pressed = down_command

    def scroll(self, event):
        if self.frm.winfo_ismapped():
            step = -int(event.delta / 120)
            if step >= 0:
                self.down(step)
            else:
                self.up(-step)

    def pack(self):
        self.frm.grid(row=self.row, column=self.column)
        self.btn_up.grid(column=0, row=0, sticky='ns')
        self.btn_down.grid(column=0, row=1, sticky='ns')
        if self.height >= 3:
            self.btn_down.grid(column=0, row=self.height - 1, sticky='ns')
            self.cnv_bar.grid(column=0, row=1, rowspan=self.height - 2)

    def unpack(self):
        self.frm.grid_forget()
        self.btn_up.grid_forget()
        if self.cnv_bar is not None:
            self.cnv_bar.grid_forget()
        self.btn_down.grid_forget()


class TEval:
    def __init__(self, master):
        self.master = master
        self.frm_lbl_eval_stack = tk.Frame(master=self.master)
        self.frm_instruction = tk.Frame(master=self.master, padx=20, pady=4)
        self.frm_content = tk.Frame(master=self.master)
        self.frm_tab = tk.Frame(master=self.frm_content)
        self.frm_arr = tk.Frame(master=self.frm_content)
        self.lbl_eval_stack = tk.Label(master=self.frm_lbl_eval_stack, text='Evaluation table:', anchor=tk.W)
        self.lbl_instruction = tk.Label(master=self.frm_instruction, padx=20,
                                        text='Scroll through each stages of the evaluation', bg='gray25', fg='white')
        self.table_lbl_exp = []
        self.arr_lbl_exp = []
        self.prev_arr_state = 0
        self.width = 0
        self.width_lbl = 0
        self.sb = TXScrollbar(self.frm_content, 2, 1, 1, 0)
        self.sb.set_button(self.scroll, self.scroll)
        self.sb.bind(self.frm_content)

    def push_to_table(self, stack):
        lbl_exp = []
        i = stack.len() - 1
        while i >= 0:
            lbl_exp.append(tk.Label(master=self.frm_tab, text=stack.list[i], relief='groove', width=self.width_lbl))
            self.sb.bind(lbl_exp[-1])
            i -= 1
        self.table_lbl_exp.append(lbl_exp.copy())

    def set_width_lbl(self, width):
        self.width_lbl = width

    def set_arr(self, expression):
        for i in expression:
            self.arr_lbl_exp.append(tk.Label(master=self.frm_arr, text=i, relief='groove', width=2))
            self.sb.bind(self.arr_lbl_exp[-1])

    def input(self, postfix_exp):
        self.delete_data()
        self.width = len(postfix_exp)
        self.set_arr(postfix_exp)
        stack = Stack()
        for i in range(self.width):
            stack.push(postfix_exp[i])
            if PostfixConverter.is_operator(postfix_exp[i]):
                str1 = stack.pop()
                str2 = stack.pop()
                str3 = stack.pop()

                if (str1 == '+' or str2 == '-') and i != self.width - 1:
                    str3 = '(' + str3
                    str2 = str2 + ')'
                str4 = str3 + str1 + str2
                stack.push(str4)
            self.push_to_table(stack)
        self.sb.init_bar(self.table_lbl_exp[-1][-1].winfo_reqheight(), self.width)

    def delete_data(self):
        self.unpack()
        self.table_lbl_exp = []
        self.arr_lbl_exp = []
        self.width = 0
        self.prev_arr_state = 0
        self.sb.tab_row = 0

    def pack(self, state):
        self.frm_lbl_eval_stack.pack(fill=tk.X)
        self.lbl_eval_stack.grid(row=0, column=0)

        self.frm_instruction.pack(fill=tk.X)
        self.lbl_instruction.pack()

        self.frm_content.pack()
        self.frm_arr.grid(row=1, column=0, columnspan=2, pady=20)
        self.arr_lbl_exp[self.prev_arr_state].config(relief='groove')
        self.arr_lbl_exp[state].config(relief='solid')
        for i in range(len(self.arr_lbl_exp)):
            self.arr_lbl_exp[i].grid(row=0, column=i, sticky=tk.W + tk.E + tk.N + tk.S)

        self.frm_tab.grid(row=2, column=0, pady=20)
        for i in range(len(self.table_lbl_exp[state])):
            self.table_lbl_exp[state][i].config(width=len(self.table_lbl_exp[-1][-1].cget('text')))
            self.table_lbl_exp[state][i].grid(row=i, column=0, sticky=tk.W + tk.E + tk.N + tk.S)

        self.sb.pack()

    def unpack(self):
        self.frm_lbl_eval_stack.pack_forget()
        self.lbl_eval_stack.grid_forget()

        self.frm_instruction.pack_forget()
        self.lbl_instruction.pack_forget()

        self.frm_content.pack_forget()
        self.frm_arr.grid_forget()
        for i in range(len(self.arr_lbl_exp)):
            self.arr_lbl_exp[i].grid_forget()

        self.frm_tab.grid_forget()
        for i in self.table_lbl_exp:
            for j in i:
                j.grid_forget()
        self.sb.unpack()

    def scroll(self):
        self.unpack()
        self.pack(self.sb.tab_row)
        self.prev_arr_state = self.sb.tab_row


class PostfixConverter:
    def __init__(self):
        self.stack = GStack()
        self.tree = TreeGenerator()
        self.output = []
        self.current_input = None
        self.row_height = 15

        self.lbl_token = []
        self.lbl_stack = []
        self.lbl_output = []
        self.sb_table = TXScrollbar(master=frm_postorder, row=0, column=1, height=self.row_height, table_row=0)
        self.sb_table.set_button(self.table_scroll, self.table_scroll)
        self.sb_table.bind(master=frm_postorder_table)

        self.btn_variable = []
        self.ety_variable_input = []
        self.lbl_current_entry = []
        self.prev_select_row = None
        self.sb_variable = TXScrollbar(master=frm_variable_table, row=0, column=0, height=10, table_row=0)
        self.sb_variable.set_button(self.var_scroll, self.var_scroll)
        self.sb_variable.bind(master=frm_variable_input)
        self.sb_variable.bind(master=frm_variable_table)

        self.tab_eval = TEval(frm_eval_table)

    @staticmethod
    def priority(token):
        if token == '^':
            return 3
        elif token == '*' or token == '/':
            return 2
        elif token == '+' or token == '-':
            return 1
        elif token == '(':
            return 0
        else:                                   # if priority less than 0, token is not operator
            return -1

    @staticmethod
    def is_operator(token):
        if token == '^' or token == '*' or token == '/' or token == '+' or token == '-':
            return True
        return False

    @staticmethod
    def is_bracket(token):
        if token == '(' or token == ')':
            return True
        return False

    @staticmethod
    def is_expression_valid(expression):
        # checks with space
        expression_size = len(expression)
        if expression_size == 0:
            return False

        for i in range(expression_size):
            i1 = expression[i]
            if not PostfixConverter.is_operator(i1) and not PostfixConverter.is_bracket(i1) and i1 != ' ':
                for j in range(i + 1, expression_size):
                    i2 = expression[j]
                    if PostfixConverter.is_operator(i2) or i2 == ')':
                        break
                    if i2 != ' ' and expression[j - 1] == ' ':
                        return False

        expression = expression.replace(' ', '')  # removes white spaces
        expression_size = len(expression)

        i1 = expression[0]      # 1st element
        i2 = expression[-1]     # Last element
        if (PostfixConverter.is_operator(i1) and not PostfixConverter.is_bracket(i1)) \
                or (PostfixConverter.is_operator(i2) and not PostfixConverter.is_bracket(i2)):
            return False         # first and last element must not be operator (except for brackets)

        counter = 0
        for i in expression:
            if i == '(':
                counter += 1
            elif i == ')':
                counter -= 1
            elif not (i.isdigit() or i.isalpha() or PostfixConverter.is_operator(i) or PostfixConverter.is_bracket(i)):
                return False

        if counter != 0:  # number of left brackets must be the same as number of right brackets
            return False

        for i in range(expression_size - 1):
            i1 = expression[i]
            i2 = expression[i + 1]

            case1 = not PostfixConverter.is_operator(i1) and i2 == '(' and i1 != '('       # i1 variable and i2 bracket
            case2 = PostfixConverter.is_operator(i1) and PostfixConverter.is_operator(i2)  # i1 and i2 operator
            case3 = i1 == ')' and not PostfixConverter.is_operator(i2) and i2 != ')'       # i1 bracket and i2 variable
            case4 = PostfixConverter.is_operator(i1) and i2 == ')'                         # i1 operator and i2 bracket
            case5 = (i1.isdigit() and i2.isalpha()) or (i1.isalpha() and i2.isdigit())     # i1 and i2 not same type
            case6 = i1.isalpha() and i2.isalpha()                                          # i1 and i2 are alpha
            case7 = i1 == '(' and i2 == ')'                                                # empty bracket
            case8 = i1 == '(' and PostfixConverter.is_operator(i2)                         # i1 bracket and i2 operator
            if case1 or case2 or case3 or case4 or case5 or case6 or case7 or case8:
                return False
        return True

    def convert(self, expression):
        self.lbl_token.insert(0, tk.Button(master=frm_postorder_table, text='Token', relief='groove',
                                           command=toggle_min_table))
        self.lbl_stack.insert(0, tk.Button(master=frm_postorder_table, text='Stack', relief='groove',
                                           command=state_2))
        self.lbl_output.insert(0, tk.Button(master=frm_postorder_table, text='Output', relief='groove',
                                            command=state_3))
        self.stack.init_table()

        for i in range(len(expression)):
            token = expression[i]
            if token == ')':
                while self.stack.top() != '(':
                    self.output.append(self.stack.pop())
                self.stack.pop()
            elif not self.is_operator(token) and token != '(':
                if token.isdigit() and i > 0:  # ensures that multiple digit numbers are single arguments
                    if expression[i - 1].isdigit():
                        self.output[-1] = self.output[-1] + token
                    else:
                        self.output.append(token)
                else:
                    self.output.append(token)
            elif token == '(':
                self.stack.push(token)
            elif self.priority(token) > self.priority(self.stack.top()):
                self.stack.push(token)
            else:
                if self.stack.top() == '^':
                    while self.stack.top() != '(' and self.stack.len() != 0:
                        self.output.append(self.stack.pop())
                else:
                    self.output.append(self.stack.pop())
                self.stack.push(token)
            self.push_to_table(token, ''.join(self.stack.get_list()), self.output)

        while self.stack.len() != 0:
            self.output.append(self.stack.pop())
            self.push_to_table('', ''.join(self.stack.get_list()), self.output)

        self.sb_table.tab_row = 0
        if len(self.lbl_output) > 16:
            self.sb_table.init_bar(pxl_h=self.lbl_output[-1].winfo_reqheight(), max_row=len(self.lbl_output) - 1)

        self.stack.sb_table.tab_row = 0
        if len(self.stack.lbl_token) > 16:
            self.stack.sb_table.init_bar(pxl_h=self.lbl_token[-1].winfo_reqheight(),
                                         max_row=len(self.stack.lbl_token) - 1)

    def table_pack(self, is_min, row):
        self.lbl_token[0].grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S)
        self.lbl_stack[0].grid(row=0, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
        self.lbl_output[0].grid(row=0, column=2, sticky=tk.W + tk.E + tk.N + tk.S)

        if is_min and len(self.lbl_output) > self.row_height:
            i = 1
            while i < self.row_height + 1:
                if i >= len(self.lbl_output):
                    break

                self.lbl_token[row + i].grid(row=i, column=0, sticky=tk.W + tk.E)
                self.lbl_stack[row + i].grid(row=i, column=1, sticky=tk.W + tk.E)
                self.lbl_output[row + i].grid(row=i, column=2, sticky=tk.W + tk.E)
                i += 1
            self.lbl_token[-1].grid(row=self.row_height, column=0, sticky=tk.W + tk.E)
            self.lbl_stack[-1].grid(row=self.row_height, column=1, sticky=tk.W + tk.E)
            self.lbl_output[-1].grid(row=self.row_height, column=2, sticky=tk.W + tk.E)

        else:
            i = 1
            while i < len(self.lbl_output):
                self.lbl_token[i].grid(row=i, column=0, sticky=tk.W + tk.E)
                self.lbl_stack[i].grid(row=i, column=1, sticky=tk.W + tk.E)
                self.lbl_output[i].grid(row=i, column=2, sticky=tk.W + tk.E)
                i += 1

    def table_unpack(self):
        for i in range(len(self.lbl_output)):
            self.lbl_token[i].grid_forget()
            self.lbl_stack[i].grid_forget()
            self.lbl_output[i].grid_forget()

    def table_scroll(self):
        self.table_unpack()
        self.table_pack(True, self.sb_table.tab_row)

    def delete_data(self):
        self.output = []
        self.current_input = None
        self.prev_select_row = None
        self.table_unpack()
        self.var_unpack()
        self.stack.table_unpack()

        for i in range(len(self.lbl_output)):
            self.lbl_token.pop()
            self.lbl_stack.pop()
            self.lbl_output.pop()

        for i in range(len(self.btn_variable)):
            self.btn_variable.pop()
            self.ety_variable_input.pop()
            self.lbl_current_entry.pop()

        while self.stack.len() != 0:
            self.stack.pop()
        self.stack.delete_data()

    def var_pack(self, row):
        i = 0
        while i < 10:
            if row + i >= len(self.btn_variable):
                break
            self.btn_variable[row + i].grid(row=i, column=0, pady=4, sticky=tk.W + tk.E)
            self.ety_variable_input[row + i].grid(row=i, column=1, pady=4)
            self.lbl_current_entry[row + i].grid(row=i, column=2, pady=4)
            i += 1

    def var_unpack(self):
        for i in range(len(self.btn_variable)):
            self.btn_variable[i].grid_forget()
            self.ety_variable_input[i].grid_forget()
            self.lbl_current_entry[i].grid_forget()

    def var_scroll(self):
        self.var_unpack()
        self.var_pack(self.sb_variable.tab_row)

    def get_postorder(self):
        return self.output

    def push_to_table(self, token, stack_top, output):
        token = '\t' + str(token) + '\t'
        if stack_top is None:
            stack_top = ' '
        stack_top = str(stack_top)

        self.lbl_token.append(tk.Label(master=frm_postorder_table, text=token, relief='groove'))
        self.lbl_stack.append(tk.Label(master=frm_postorder_table, text=stack_top, relief='groove'))
        self.lbl_output.append(tk.Label(master=frm_postorder_table, text=output, relief='groove', anchor=tk.W))

        game.sb_table.bind(self.lbl_token[-1])
        game.sb_table.bind(self.lbl_stack[-1])
        game.sb_table.bind(self.lbl_output[-1])

    @staticmethod
    def can_eval(expression):
        expression = expression.replace(' ', '')
        for i in expression:
            if i.isalpha():
                return False
        return True

    def push_to_variable(self, variable, row):
        # variable = '\t' + str(variable) + '\t'
        variable = str(variable)

        self.btn_variable.append(tk.Button(master=frm_variable_input, text=variable, relief='solid', padx=10,
                                           command=lambda: self.update_ety_variable(row)))
        self.ety_variable_input.append(tk.Entry(master=frm_variable_input, width=10))
        self.ety_variable_input[row].bind('<Return>', lambda event: self.switch_entry(row))
        self.lbl_current_entry.append(tk.Label(master=frm_variable_input))

        game.sb_variable.bind(self.btn_variable[-1])
        game.sb_variable.bind(self.ety_variable_input[-1])
        game.sb_variable.bind(self.lbl_current_entry[-1])

    def update_ety_variable(self, row):
        if self.ety_variable_input[row].select_present():
            self.clear_ety_variable(row)
            self.lbl_current_entry[row].config(text=': ')
        self.select_ety_variable(row)

    def clear_ety_variable(self, row):
        self.ety_variable_input[row].delete(0, tk.END)
        lbl_evaluation_result.config(text='Evaluation result: ?')

    def select_ety_variable(self, row):
        if self.prev_select_row is not None:
            self.ety_variable_input[self.prev_select_row].select_clear()
        self.ety_variable_input[row].focus_set()
        self.ety_variable_input[row].select_range(0, tk.END)
        self.prev_select_row = row

    def init_current_entry(self):
        for i in self.lbl_current_entry:
            i.config(text=': ', fg='gray50')

    def switch_entry(self, row):
        if row + 1 >= len(self.ety_variable_input):
            btn_evaluate.focus_set()
        else:
            if row >= 10 - 1 and self.sb_variable.tab_row != len(self.ety_variable_input) - 10:
                self.sb_variable.tab_row = row - 8
                self.var_scroll()
                self.sb_variable.update_bar()
            self.select_ety_variable(row + 1)

    def is_var_exist(self, variable):
        for i in self.btn_variable:
            if i.cget('text') == variable:
                return True
        return False

    def update_tree(self):
        cnv_tree.delete('all')
        if PostfixConverter.is_expression_valid(game.current_input):
            self.tree.input(self.output)


def update_output():
    math_input = ety_textbox.get()

    if game.current_input != math_input:
        game.delete_data()

        flag[2] = False
        flag[3] = False
        flag[4] = False
        math_input = math_input.replace('\t', ' ')      # removes tab
        math_input = math_input.replace('\n', ' ')      # removes new line
        math_input = math_input.replace('\x1f', ' ')    # removes unit separator

        if math_input.replace(' ', '') == '':
            lbl_result.config(text='Input is empty!')
            game.current_input = ''

        elif not game.is_expression_valid(math_input):
            lbl_result.config(text='Input is invalid!')
            game.current_input = math_input

        else:
            flag[2] = True
            game.current_input = math_input.replace(' ', '')
            lbl_current_input.config(text='Current Input: ' + game.current_input)

            game.convert(game.current_input)

            result = 'Postfix result = ' + '  '.join(game.get_postorder())
            lbl_result.config(text=result)

            result = 'Evaluation result: '
            if game.can_eval(game.current_input):
                result += evaluate(game.get_postorder())
                lbl_evaluation_result.config(text=result)
            else:
                flag[3] = True

                game.tab_eval.set_width_lbl(len(game.current_input))
                game.tab_eval.input(game.get_postorder())
                result += '?'
                lbl_evaluation_result.config(text=result)

                row = 0
                for i in range(len(game.current_input)):
                    var = game.current_input[i]
                    if var.isalpha():
                        if not game.is_var_exist(var):
                            game.push_to_variable(var, row)
                            row += 1
                game.sb_variable.tab_row = 0
                game.sb_variable.init_bar(pxl_h=game.btn_variable[-1].winfo_reqheight() + 20,
                                          max_row=len(game.btn_variable))
                game.init_current_entry()
                game.ety_variable_input[0].focus_set()
                btn_evaluate.grid(row=row, column=1)

        if flag[1] == 2:
            state_2()
        elif flag[1] == 3:
            state_3()
        else:
            state_1()


def output_pack():
    if flag[1] > 0:
        frm_main_lower.pack(fill=tk.X)
        if flag[1] == 1:
            if flag[2]:
                frm_current_input.pack(fill=tk.X)
                lbl_current_input.pack(side='left')

            frm_main_lower2.pack(fill=tk.X)

            if flag[3]:
                frm_output.pack(fill=tk.X, side='left')
                frm_variable.pack(fill=tk.BOTH)
            else:
                frm_output.pack(fill=tk.X)

            frm_lbl_output.pack(fill=tk.X)
            lbl_output.pack(side='left')

            if flag[2]:
                frm_postorder.pack()
                frm_postorder_table.grid(row=0, column=0)
                if flag[4]:
                    game.table_pack(is_min=True, row=game.sb_table.tab_row)
                    if len(game.lbl_output) > 16:
                        game.sb_table.pack()
                else:
                    game.table_pack(is_min=False, row=None)

            frm_result.pack()
            lbl_result.pack()

            if flag[2]:
                lbl_evaluation_result.pack()

            btn_clear.pack()

            frm_lbl_variable.pack(fill=tk.X)
            lbl_variable.pack(side='left')
            lbl_instruction2.pack()
            frm_variable_table.pack()
            frm_variable_input.grid(row=0, column=1, padx=8)
            game.var_pack(row=game.sb_variable.tab_row)
            if len(game.btn_variable) > 10:
                game.sb_variable.pack()
            lbl_invalid_var.pack()
        elif flag[1] == 2:
            frm_stack.pack(side='left')
            frm_lbl_stack.pack(fill=tk.X)
            lbl_stack.pack(side='left')
            frm_stack_output.pack()
            frm_stack_table.grid(row=0, column=0)
            game.stack.table_pack(row=game.stack.sb_table.tab_row)
            frm_eval_table.pack(side='right')
            game.tab_eval.pack(game.tab_eval.sb.tab_row)
            if len(game.stack.lbl_token) > 16:
                game.stack.sb_table.pack()
        elif flag[1] == 3:
            frm_tree.pack(fill=tk.X)
            frm_lbl_tree.pack(fill=tk.X)
            lbl_tree.pack(side='left')
            frm_tree_space.pack()
            cnv_tree.grid(row=0, column=0)
            lbl_tree_result.grid(row=1, column=0, pady=4)
            btn_tree_back.grid(row=2, column=0)


def output_unpack():
    frm_main_lower.pack_forget()

    frm_current_input.pack_forget()
    lbl_current_input.pack_forget()

    frm_main_lower2.pack_forget()

    frm_output.pack_forget()
    frm_lbl_output.pack_forget()
    lbl_output.pack_forget()
    frm_postorder.pack_forget()
    frm_postorder_table.grid_forget()
    game.table_unpack()
    game.sb_table.unpack()
    frm_result.pack_forget()
    lbl_result.pack_forget()
    lbl_evaluation_result.pack_forget()
    btn_clear.pack_forget()

    frm_variable.pack_forget()
    frm_lbl_variable.pack_forget()
    lbl_variable.pack_forget()
    lbl_instruction2.pack_forget()
    frm_variable_table.pack_forget()
    frm_variable_input.grid_forget()
    game.var_unpack()
    game.sb_variable.unpack()
    lbl_invalid_var.pack_forget()

    frm_stack.pack_forget()
    frm_lbl_stack.pack_forget()
    lbl_stack.pack_forget()
    frm_stack_output.pack_forget()
    frm_stack_table.grid_forget()
    game.stack.table_unpack()
    game.stack.sb_table.unpack()
    frm_eval_table.pack_forget()
    game.tab_eval.unpack()

    frm_tree.pack_forget()
    frm_lbl_tree.pack_forget()
    lbl_tree.pack_forget()
    frm_tree_space.pack_forget()
    cnv_tree.grid_forget()
    lbl_tree_result.grid_forget()
    btn_tree_back.grid_forget()


def initial_pack():
    frm_root.pack()
    btn_info.place(relx=1, rely=0, anchor='ne')
    if not flag[0]:
        frm_instruction.pack(fill=tk.X)
        lbl_instruction.pack(fill=tk.X)

        frm_main.pack(fill=tk.X)

        frm_lbl_input.pack(fill=tk.X)
        lbl_input.pack(side='left', fill=tk.X)

        frm_textbox.pack(fill=tk.X)
        ety_textbox.pack(side='left')
        btn_convert.pack(side='right')
    else:
        frm_instruction.pack_forget()
        lbl_instruction.pack_forget()

        frm_main.pack_forget()

        frm_lbl_input.pack_forget()
        lbl_input.pack_forget()

        frm_textbox.pack_forget()
        ety_textbox.pack_forget()
        btn_convert.pack_forget()


def toggle_info():
    if flag[0]:
        flag[0] = False
        btn_info.config(fg='black', bg='#F0F0F0')
        frm_info.pack_forget()
        lbl_group_member.pack_forget()
        lbl_names.pack_forget()
        initial_pack()
        output_pack()
    else:
        flag[0] = True
        btn_info.config(fg='white', bg='gray25')
        frm_info.pack()
        lbl_group_member.pack()
        lbl_names.pack(side='left')
        output_unpack()
        initial_pack()


def clear_io():
    flag[1] = 0
    output_unpack()
    game.current_input = None
    ety_textbox.focus_set()
    ety_textbox.select_range(0, tk.END)


def evaluate(expression):

    game.tab_eval.delete_data()
    game.tab_eval.width = len(expression)
    game.tab_eval.set_arr(expression)
    stack = Stack()
    i = 0
    while i < len(expression):
        stack.push(expression[i])
        if game.is_operator(expression[i]):
            stack.pop()
            i2 = float(stack.pop())
            i1 = float(stack.pop())
            try:
                if expression[i] == '+':
                    stack.push(str(i1 + i2))
                elif expression[i] == '-':
                    stack.push(str(i1 - i2))
                elif expression[i] == '*':
                    stack.push(str(i1 * i2))
                elif expression[i] == '/':
                    if i2 == 0:
                        stack.push('UNDEFINED')
                        while i < len(expression):
                            game.tab_eval.push_to_table(stack)
                            i += 1
                        break
                    else:
                        stack.push(str(i1 / i2))
                elif expression[i] == '^':
                    stack.push(str(pow(i1, i2)))
            except OverflowError:
                stack.push('OVERFLOW')
                while i < len(expression):
                    game.tab_eval.push_to_table(stack)
                    i += 1
                break
        game.tab_eval.push_to_table(stack)
        i += 1
    game.tab_eval.sb.init_bar(game.tab_eval.table_lbl_exp[-1][-1].winfo_reqheight(), game.tab_eval.width)
    return str(stack.top())


def is_variable_number(ety):
    for i in range(len(ety)):
        game.lbl_current_entry[i].config(text=": " + ety[i].get())
        try:
            float(ety[i].get())
        except ValueError:
            game.select_ety_variable(i)
            game.lbl_current_entry[i].config(fg='red')
            game.sb_variable.tab_row = i
            if i + 10 >= len(game.btn_variable) > 10:
                game.sb_variable.tab_row = len(game.btn_variable) - 10
            game.var_unpack()
            game.var_pack(game.sb_variable.tab_row)
            game.sb_variable.update_bar()
            return False
    window.focus_set()  # remove focus from all entry
    return True


def update_eval():
    output = game.get_postorder().copy()
    ety = game.ety_variable_input
    game.init_current_entry()

    if is_variable_number(ety):
        for i in range(len(ety)):
            for j in range(len(output)):
                if output[j] == game.btn_variable[i].cget('text'):
                    output[j] = ety[i].get()

        result = 'Evaluation result: ' + evaluate(output)
        lbl_invalid_var.config(text='')
    else:
        result = 'Evaluation result: ?'
        lbl_invalid_var.config(text='Invalid!\nInput must be numbers')

    lbl_result.pack_forget()
    lbl_result.pack()

    lbl_evaluation_result.config(text=result)
    lbl_evaluation_result.pack_forget()
    lbl_evaluation_result.pack()


def toggle_min_table():
    if flag[4]:
        flag[4] = False
        game.lbl_token[0].config(fg='black')
    else:
        flag[4] = True
        game.lbl_token[0].config(fg='gray50')

    output_unpack()
    output_pack()


def state_1():
    flag[1] = 1
    output_unpack()
    output_pack()


def state_2():
    flag[1] = 2
    output_unpack()
    output_pack()


def state_3():
    flag[1] = 3

    game.update_tree()
    lbl_tree_result.config(text='Postfix Result: ' + '  '.join(game.get_postorder()))
    output_unpack()
    output_pack()


# GUI Creation
window = tk.Tk()
window.title('Infix to Postfix converter')
window.resizable(width=False, height=False)

# Constants
INSTRUCTION_WIDTH = 60
TEXTBOX_WIDTH = 80

# Initialization of Window Widgets
frm_root = tk.Frame(master=window)
btn_info = tk.Label(master=window, text='?')
frm_info = tk.Frame(master=frm_root, width=400, height=400, padx=10, pady=10, bg='gray25')
lbl_group_member = tk.Label(master=frm_info, font='helvetic 14 bold',
                            text='Group Members (2)\t\t\t\t', anchor=tk.W, bg='gray25', fg='white')
lbl_names = tk.Label(master=frm_info,
                     font='helvetic 12',
                     text='Muhammad Firdaus Bin Asrar\t\t\t\t2019857\n'
                          'Muhammad Darwish Bin Mohd Sukri\t\t\t2014169\n'
                          'Muhamad Adzim Bin Rosly\t\t\t\t2013413',
                     anchor=tk.W, bg='gray25', fg='white')

frm_instruction = tk.Frame(master=frm_root, padx=20, pady=8)
lbl_instruction = tk.Label(master=frm_instruction,
                           text='Enter an infix expression in the entry below and\n'
                                'press the \"Convert\" button or ENTER for postfix conversion',
                           width=INSTRUCTION_WIDTH, bg='gray25', fg='white')

frm_main = tk.Frame(master=frm_root, padx=25, pady=4)
frm_lbl_input = tk.Frame(master=frm_main)
lbl_input = tk.Label(master=frm_lbl_input, text='Input:')
frm_textbox = tk.Frame(master=frm_main, pady=4)
ety_textbox = tk.Entry(master=frm_textbox, width=TEXTBOX_WIDTH, exportselection=True)
btn_convert = tk.Button(master=frm_textbox, borderwidth=2, text='Convert', command=update_output)
frm_main_lower = tk.Frame(master=frm_main, padx=4, pady=4, bd=2, relief='solid')
frm_current_input = tk.Frame(master=frm_main_lower)
lbl_current_input = tk.Label(master=frm_current_input, fg='gray50')
frm_main_lower2 = tk.Frame(master=frm_main_lower)
frm_output = tk.Frame(master=frm_main_lower2)
frm_lbl_output = tk.Frame(master=frm_output)
lbl_output = tk.Label(master=frm_lbl_output, text='Output:')
frm_postorder = tk.Frame(master=frm_output, pady=4)
frm_postorder_table = tk.Frame(master=frm_postorder, pady=4)

# Conversion from infix to postfix
frm_result = tk.Frame(master=frm_output, bd=1, relief='solid')
lbl_result = tk.Label(master=frm_result, pady=8, padx=4)
lbl_evaluation_result = tk.Label(master=frm_result, pady=8, padx=4)
btn_clear = tk.Button(master=frm_output, borderwidth=2, text='Clear', command=clear_io)
frm_variable = tk.Frame(master=frm_main_lower2, padx=4)
frm_lbl_variable = tk.Frame(master=frm_variable)
lbl_variable = tk.Label(master=frm_lbl_variable, text='Variable(s):')
lbl_instruction2 = tk.Label(master=frm_variable,
                            text='Input number for substitution of variable(s).\n'
                                 'Press ENTER to switch entry or evaluate',
                            pady=4, padx=4, bg='gray25', fg='white')
frm_variable_table = tk.Frame(master=frm_variable, pady=4)
frm_variable_input = tk.Frame(master=frm_variable_table)
btn_evaluate = tk.Button(master=frm_variable_input, borderwidth=2, text='Evaluate', command=update_eval)
lbl_invalid_var = tk.Label(master=frm_variable)

frm_stack = tk.Frame(master=frm_main_lower)
frm_lbl_stack = tk.Frame(master=frm_stack)
lbl_stack = tk.Label(master=frm_lbl_stack, text='Stack Table:')
frm_stack_output = tk.Frame(master=frm_stack, pady=4)
frm_stack_table = tk.Frame(master=frm_stack_output)
btn_stack_back = tk.Button(master=frm_stack_output, borderwidth=2, text='back', command=state_1)

frm_eval_table = tk.Frame(master=frm_main_lower)

frm_tree = tk.Frame(master=frm_main_lower)
frm_lbl_tree = tk.Frame(master=frm_tree)
lbl_tree = tk.Label(master=frm_lbl_tree, text='Tree Diagram:')
frm_tree_space = tk.Frame(master=frm_tree, pady=4)
cnv_tree = tk.Canvas(master=frm_tree_space)
lbl_tree_result = tk.Label(master=frm_tree_space, padx=4, pady=4, relief='solid')
btn_tree_back = tk.Button(master=frm_tree_space, borderwidth=2, text='back', command=state_1)

# initialization
game = PostfixConverter()
flag = [False, 0, False, False, False]
initial_pack()

btn_info.bind('<Button-1>', lambda event: toggle_info())
ety_textbox.focus_set()
ety_textbox.bind('<Return>', lambda event: update_output())
ety_textbox.bind('Double-1', lambda event: ety_textbox.select_range(0, tk.END))
btn_evaluate.bind('<Return>', lambda event: update_eval())

window.mainloop()

# Example input
# math_input = "7*8-(4+24)^2+5"
# math_input = "A*B-(C+24)^2+D"
# math_input = "A*B-(2+D)+A*B-(C+4)"
# math_input = "A*B-(C+24)^2+D+A*B-(C+24)^2+D"
# math_input = "A*B-(C+4)^2+D+A*B-(C+4)^2+D+A*B-(C+4)^2+D+A*B-(C+4)^2+D+A*B-(C+4)^2+D+A*B-(C+4)^2+D"
# math_input = "A^(B^(C^(D^(E^(F^(G^(H^(I^J))))))))"
