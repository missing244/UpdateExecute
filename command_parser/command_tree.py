from . import BaseMatch,SpecialMatch

Command_Tree = SpecialMatch.Command_Root().add_leaves(
    BaseMatch.KeyWord("Command_Start","/"),
    BaseMatch.Char("Command","execute"),
    BaseMatch.Char("Command","setblock").add_leaves(
        *SpecialMatch.Pos_Tree(
            BaseMatch.AnyString("Block_ID").add_leaves(
                SpecialMatch.BE_BlockState_Tree( 
                    BaseMatch.Enum("Setblock_Mode","replace","keep","destroy").add_leaves( BaseMatch.End_Tag() ),
                    BaseMatch.End_Tag() 
                ),
                BaseMatch.Int("Block_Data").add_leaves(
                    BaseMatch.Enum("Setblock_Mode","replace","keep","destroy").add_leaves( BaseMatch.End_Tag() ),
                    BaseMatch.End_Tag() 
                ),
                BaseMatch.End_Tag()
            )
        )
    ),
    BaseMatch.Char("Command","testforblock").add_leaves(
        *SpecialMatch.Pos_Tree(
            BaseMatch.AnyString("Block_ID").add_leaves(
                SpecialMatch.BE_BlockState_Tree( BaseMatch.End_Tag() ),
                BaseMatch.Int("Block_Data").add_leaves( BaseMatch.End_Tag() ),
                BaseMatch.End_Tag()
            )
        )    
    ),
    BaseMatch.Char("Command","clone").add_leaves(
        *SpecialMatch.Pos_Tree(
            *SpecialMatch.Pos_Tree(
                *SpecialMatch.Pos_Tree(
                    BaseMatch.Enum("Mask_Mode","replace","masked").add_leaves(
                        BaseMatch.Enum("Clone_Mode","force","move","normal").add_leaves( BaseMatch.End_Tag() ),
                        BaseMatch.End_Tag()
                    ),
                    BaseMatch.Enum("Mask_Mode:指定拷贝方块","filtered").add_leaves(
                        BaseMatch.Enum("Clone_Mode","force","move","normal").add_leaves(
                            BaseMatch.AnyString("Block_ID").add_leaves(
                                SpecialMatch.BE_BlockState_Tree( BaseMatch.End_Tag() ),
                                BaseMatch.Int("Block_Data").add_leaves( BaseMatch.End_Tag() )
                            )
                        )
                    ),
                    BaseMatch.End_Tag()
                )
            )
        )    
    ),
    BaseMatch.Char("Command","fill").add_leaves(
        *SpecialMatch.Pos_Tree(
            *SpecialMatch.Pos_Tree(
                BaseMatch.AnyString("Block_ID").add_leaves(
                    SpecialMatch.BE_BlockState_Tree( 
                        BaseMatch.Char("Fill_Mode","replace").add_leaves(
                            BaseMatch.AnyString("Block_ID").add_leaves(
                                SpecialMatch.BE_BlockState_Tree( BaseMatch.End_Tag() )
                            ),
                            BaseMatch.End_Tag()
                        ),
                        BaseMatch.Enum("Fill_Mode","hollow","keep","outline","replace").add_leaves( BaseMatch.End_Tag() ),
                        BaseMatch.End_Tag()
                    ),
                    BaseMatch.Int("Block_Data").add_leaves( 
                        BaseMatch.Char("Fill_Mode","replace").add_leaves(
                            BaseMatch.AnyString("Block_ID").add_leaves(
                                BaseMatch.Int("Block_Data").add_leaves( BaseMatch.End_Tag() )
                            ),
                            BaseMatch.End_Tag()
                        ),
                        BaseMatch.Enum("Fill_Mode","hollow","keep","outline","replace").add_leaves( BaseMatch.End_Tag() ),
                        BaseMatch.End_Tag()
                    ),
                    BaseMatch.End_Tag()
                )
            )
        )    
    ),
    BaseMatch.AnyMsg("Any_Command").add_leaves(BaseMatch.End_Tag())
)
Command_Tree.tree_leaves[0].add_leaves(
    *Command_Tree.tree_leaves
)
Command_Tree.tree_leaves[1].add_leaves(
    *SpecialMatch.BE_Selector_Tree(
        *SpecialMatch.Pos_Tree(
            BaseMatch.Char("Block_Test","detect").add_leaves(
                *SpecialMatch.Pos_Tree(
                    BaseMatch.AnyString("Block_ID").add_leaves(
                        BaseMatch.Int("Block_Data").add_leaves( *Command_Tree.tree_leaves )
                    )
                )
            ),
            *Command_Tree.tree_leaves
        )
    )
)














