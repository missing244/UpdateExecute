from command_parser import ParserSystem,CommandTree,CommandTransfor
import heartrate,time
#heartrate.trace(browser=1)


str1 = 'execute@s[r = 1, name="阿大的那",hasitem=[{item=aaa}]] ~ ~ ~ detect ~ ~ ~ bedrock 1 say aaa'
#str1 = ''
Tokenazier = ParserSystem.Command_Parser(CommandTree.Command_Tree)
Token_List = Tokenazier.parser(str1)

if isinstance(Token_List,tuple) : 
    print("######################## ERROR #########################")
    print(Token_List[0])
    print("########################################################")
else : 
    print("######################## Token #########################")
    print(Token_List)
    print("########################################################")
    command_transfor = CommandTransfor.Start_Transformer(Token_List)
    print(command_transfor)
exit()