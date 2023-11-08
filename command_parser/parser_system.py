"""
命令词法器系统
class Command_Parser
"""

from . import BaseMatch,SpecialMatch

from typing import Dict,Union,List,Tuple,Literal
import re,traceback


class Command_Parser :
    """
    词法器
    ------------------------
    实例化参数
    Tree : SpecialMatch.Command_Root类开始嵌套的命令树
    separator : 一个分隔字符
    separator_count : 每段匹配机构之间需要需要相隔多少分隔符
    """

    def __init__(self,Tree:SpecialMatch.Command_Root,separator:str=" ", separator_count:int=None) -> None:
        if not isinstance(Tree,SpecialMatch.Command_Root) : raise TypeError("Tree 参数只能为 SpecialMatch.Command_Root 类")

        if not isinstance(separator,str) : raise TypeError("separator 参数只能为字符串")
        if separator.__len__() != 1 : raise Exception("separator 参数应该只存在一个字符")

        if not isinstance(separator_count,(type(None), int)) : raise TypeError("separator_count 参数只能为None或者整数")
        if isinstance(separator_count,int) and separator_count < 1 : raise Exception("separator_count 参数应该为正整数")
        
        self.Tree = Tree
        self.separator = separator
        self.separator_count = separator_count
        if separator_count == None : self.separator_re_match = re.compile("[%s]{0,}" % BaseMatch.string_to_rematch(separator))
        else : self.separator_re_match = re.compile("[%s]{%s,%s}" % (BaseMatch.string_to_rematch(separator), separator_count, separator_count))
        self.no_match_error1 = re.compile("[^%s]{1,}" % BaseMatch.TERMINATOR_RE)
        self.no_match_error2 = re.compile(".{0,1}")

        self.current_leaves = Tree
        self.before_leaves = None

    def reset_parser_tree(self) :
        self.current_leaves = self.Tree
        self.before_leaves = None

    def _jump_space(self,s:str,s_pointer:int) :
        return self.separator_re_match.match(s,s_pointer)

    def _get_auto_complete(self,e:Exception) :
        _str1 = {}
        for i in self.current_leaves.tree_leaves : _str1.update(i._auto_complete())
        re_match1 = re.compile(BaseMatch.string_to_rematch(e.word))
        for i in list(_str1.keys()) :
            a = re_match1.search(i)
            if a == None : del _str1[i]

        if 0 :
            _str2 = {}
            if self.before_leaves :
                self.before_leaves.tree_leaves : _str2.update(i._auto_complete())
                re_match2 = re.compile(BaseMatch.string_to_rematch(self.Token_list[-1]["token"].group()))
                for i in list(_str2.keys()) :
                    a = re_match2.search(i)
                    if a == None : del _str2[i]

            _str1.update(_str2)
        return _str1

    def _parser(self,command_str:str) -> List[Dict[Literal["type","token"],Union[str,re.Match]]] :
        command_str_pointer = 0 ; self.Token_list = Token_list = []

        while 1 :
            if not len(self.current_leaves.tree_leaves) : break

            is_not_successs = True
            for i in self.current_leaves.tree_leaves :
                try : a = i._match_string(command_str,command_str_pointer)
                except Exception as e : continue
                else : 
                    is_not_successs = False
                    self.before_leaves = self.current_leaves
                    self.current_leaves = i
                    if isinstance(i,BaseMatch.End_Tag) : break
                    command_str_pointer = a["token"].end()
                    Token_list.append(a)
                    break

            if is_not_successs : 
                _m_ = self.no_match_error1.match(command_str,command_str_pointer)
                if _m_ == None : _m_ = self.no_match_error2.match(command_str,command_str_pointer)
                raise BaseMatch.Not_Match("语法错误：>>%s<< 非期望的参数" % _m_.group(), pos=(_m_.start(),_m_.end()), word=_m_.group())
            
            if isinstance(self.current_leaves,BaseMatch.End_Tag) : break
            command_str_pointer = self._jump_space(command_str,command_str_pointer).end()

        return Token_list

    def parser(self,command_str:str) -> Union[List[Dict[Literal["type","token"],Union[str,re.Match]]],Tuple[str]] :
        """
        return List[ {"type":str, "token":re.Match} ]
        or
        return Tuple[ Error_str, ]\n
        ------------------------------------
        Tuple 意味着 错误信息
        """
        self.reset_parser_tree()
        if command_str.__len__() > 7500 : return ("输入错误：无法转换过长的命令",)

        try : a = self._parser(command_str)
        except Exception as e : 
            s = "%s\n错误位于字符%s至%s" % (e.args[0], e.pos[0], e.pos[1])
            return (s,)
        else : 
            for _,token in enumerate(list(a)) :
                if token["type"] == "Command_Start" : a.remove(token)
            return a













