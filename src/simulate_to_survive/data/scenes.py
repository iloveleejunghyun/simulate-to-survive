"""
Scene data for Simulate to Survive
Contains all scene content, choices, and branching logic
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class ChoiceType(Enum):
    """Choice types"""
    EMOTION = "emotion"      # 影响情感值
    STORY = "story"          # 影响剧情分支
    SYSTEM = "system"        # 影响系统状态

@dataclass
class Choice:
    """Individual choice option"""
    id: str
    text: str
    choice_type: ChoiceType
    emotion_effects: Dict[str, int] = None
    next_scene: str = None
    conditions: Dict[str, Any] = None

@dataclass
class SceneEvent:
    """Scene event with text and choices"""
    id: str
    text: str
    choices: List[Choice]
    background: str = None
    ambient_sound: str = None
    music: str = None

@dataclass
class Scene:
    """Complete scene definition"""
    id: str
    title: str
    description: str
    events: List[SceneEvent]
    background: str = None
    ambient_sound: str = None
    music: str = None

# 序章第一段：无力感的建立
CH0_PHASE_01 = Scene(
    id="CH0_PHASE_01",
    title="晨雾·青云宗演武场",
    description="清晨，薄雾笼罩演武场。数十名弟子整齐练剑，剑气纵横。主角独自在角落，木剑颤抖，动作生涩。",
    background="morning_fog",
    ambient_sound="environment_gentle-rain",
    events=[
        SceneEvent(
            id="CH0_E01",
            text="【晨雾·青云宗演武场】\n\n薄雾笼罩着青云宗的演武场，数十名弟子正在晨练。剑气纵横，剑光如虹。\n\n而你，独自站在角落，手中的木剑微微颤抖。\n\n首席师兄一剑劈开三丈外的落叶，剑气如虹，引来阵阵喝彩。\n\n而你，连最基本的剑式都做不好。",
            choices=[
                Choice(
                    id="CH0_CHOICE_01A",
                    text="我...我再练练",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"执念": 10}
                ),
                Choice(
                    id="CH0_CHOICE_01B", 
                    text="总有一天我会证明给你们看",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"愤怒": 15}
                ),
                Choice(
                    id="CH0_CHOICE_01C",
                    text="沉默不语",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"压抑": 12}
                )
            ]
        ),
        SceneEvent(
            id="CH0_E02",
            text="剑术考核开始了。\n\n你再次垫底。\n\n同门弟子当众嘲笑：\"废物，连剑都握不稳！\"\n\n阿璃偷偷想递给你一颗丹药，却被她父亲严厉地打断了。\n\n你感到无比的无力。",
            choices=[
                Choice(
                    id="CH0_CHOICE_02A",
                    text="握紧拳头，默默承受",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"压抑": 8, "执念": 5}
                ),
                Choice(
                    id="CH0_CHOICE_02B",
                    text="愤怒地瞪着嘲笑你的人",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"愤怒": 12, "执念": 8}
                ),
                Choice(
                    id="CH0_CHOICE_02C",
                    text="看向阿璃，心中五味杂陈",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"情感": 10, "压抑": 5}
                )
            ]
        ),
        SceneEvent(
            id="CH0_E03",
            text="考核结束后，你独自坐在演武场的角落。\n\n远处传来弟子们的欢声笑语，而你只能看着手中的木剑发呆。\n\n这把木剑已经陪伴你三年了，却依然如新。\n\n因为你，连让它磨损的资格都没有。",
            choices=[
                Choice(
                    id="CH0_CHOICE_03A",
                    text="继续练习，哪怕只是徒劳",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"执念": 15, "决心": 10}
                ),
                Choice(
                    id="CH0_CHOICE_03B",
                    text="思考为什么自己这么弱",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"压抑": 10, "执念": 8}
                ),
                Choice(
                    id="CH0_CHOICE_03C",
                    text="回忆阿璃的鼓励",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"情感": 15, "决心": 5}
                )
            ]
        )
    ]
)

# 序章第二段：冲突的激化
CH0_PHASE_02 = Scene(
    id="CH0_PHASE_02",
    title="暮色·宗门庭院",
    description="傍晚，夕阳西下。父亲林苍澜背对而立，玄色道袍被晚风吹动。石桌上散落断裂的木剑和药碗。",
    background="evening_courtyard",
    ambient_sound="environment_gentle-rain",
    events=[
        SceneEvent(
            id="CH0_E04",
            text="【暮色·宗门庭院】\n\n傍晚时分，你被叫到宗门庭院。\n\n父亲林苍澜背对着你，玄色道袍被晚风吹动。石桌上散落着你断裂的木剑和药碗。\n\n远处传来弟子们的欢声笑语，与这里的压抑形成鲜明对比。",
            choices=[
                Choice(
                    id="CH0_CHOICE_04A",
                    text="低头等待训斥",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"压抑": 10}
                ),
                Choice(
                    id="CH0_CHOICE_04B",
                    text="抬头直视父亲",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"愤怒": 8, "决心": 5}
                ),
                Choice(
                    id="CH0_CHOICE_04C",
                    text="看向断裂的木剑",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"执念": 12}
                )
            ]
        ),
        SceneEvent(
            id="CH0_E05",
            text="父亲缓缓转身，目光如刀。\n\n\"三年了，\"他的声音低沉而压抑，\"你连最基本的剑式都练不好。\"\n\n他指着石桌上的断裂木剑：\"连木剑都能被你握断，你还有什么用？\"\n\n\"三年内练不到筑基境，就滚出青云宗。\"",
            choices=[
                Choice(
                    id="CH0_CHOICE_05A",
                    text="爹，我保证会努力",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"压抑": 5, "执念": 10}
                ),
                Choice(
                    id="CH0_CHOICE_05B",
                    text="您是不是早就想赶我走？",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"愤怒": 15, "压抑": 8}
                ),
                Choice(
                    id="CH0_CHOICE_05C",
                    text="我会证明给您看的",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"决心": 20, "执念": 12}
                )
            ]
        ),
        SceneEvent(
            id="CH0_E06",
            text="阿璃的父亲也来了。\n\n\"连剑都握不稳，将来魔族来了只能当炮灰。\"他冷笑着说，\"阿璃，少跟这种拖后腿的浪费时间。\"\n\n阿璃欲言又止，默默握紧腰间的右半玉佩。\n\n你感到前所未有的羞辱和愤怒。",
            choices=[
                Choice(
                    id="CH0_CHOICE_06A",
                    text="握紧拳头，强忍怒火",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"愤怒": 20, "执念": 15}
                ),
                Choice(
                    id="CH0_CHOICE_06B",
                    text="看向阿璃，寻求支持",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"情感": 15, "压抑": 10}
                ),
                Choice(
                    id="CH0_CHOICE_06C",
                    text="在心中发誓要变强",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"决心": 25, "执念": 20}
                )
            ]
        )
    ]
)

# 序章第三段：内心的挣扎
CH0_PHASE_03 = Scene(
    id="CH0_PHASE_03",
    title="黄昏·后山小径",
    description="黄昏时分，夕阳如血。主角独自坐在后山石阶上，手中握着阿璃的右半玉佩。远处传来弟子们的练剑声和笑声。",
    background="sunset_hillside",
    ambient_sound="environment_gentle-rain",
    events=[
        SceneEvent(
            id="CH0_E07",
            text="【黄昏·后山小径】\n\n黄昏时分，你独自来到后山小径。\n\n夕阳如血，染红了整个天空。你坐在石阶上，手中握着阿璃的右半玉佩。\n\n远处传来弟子们的练剑声和笑声，而你只能在这里独自沉思。",
            choices=[
                Choice(
                    id="CH0_CHOICE_07A",
                    text="回忆与阿璃的过往",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"情感": 20}
                ),
                Choice(
                    id="CH0_CHOICE_07B",
                    text="思考自己的处境",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"压抑": 15, "执念": 10}
                ),
                Choice(
                    id="CH0_CHOICE_07C",
                    text="看着玉佩发呆",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"情感": 10, "执念": 8}
                )
            ]
        ),
        SceneEvent(
            id="CH0_E08",
            text="你想起三年前，阿璃将右半玉佩交给你时的情景。\n\n\"这是我们的约定，\"她说，\"无论发生什么，我们都要在一起。\"\n\n而现在，你连保护她的能力都没有。\n\n你想起父亲的话：\"三年内练不到筑基境，就滚出青云宗。\"\n\n你想起阿璃父亲的嘲讽：\"连剑都握不稳，将来魔族来了只能当炮灰。\"",
            choices=[
                Choice(
                    id="CH0_CHOICE_08A",
                    text="回忆与阿璃的甜蜜时光",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"情感": 25, "决心": 15}
                ),
                Choice(
                    id="CH0_CHOICE_08B",
                    text="回忆被嘲笑的痛苦经历",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"愤怒": 20, "执念": 15}
                ),
                Choice(
                    id="CH0_CHOICE_08C",
                    text="思考变强的可能性",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"决心": 30, "执念": 20}
                )
            ]
        ),
        SceneEvent(
            id="CH0_E09",
            text="夜幕降临，你依然坐在石阶上。\n\n手中的玉佩在月光下微微发光，仿佛在诉说着什么。\n\n你想起阿璃今天欲言又止的样子，想起她父亲的话，想起自己的无能。\n\n你感到前所未有的孤独和绝望，但内心深处，还有一丝不甘。",
            choices=[
                Choice(
                    id="CH0_CHOICE_09A",
                    text="我要变强，保护阿璃",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"决心": 35, "执念": 25}
                ),
                Choice(
                    id="CH0_CHOICE_09B",
                    text="也许我真的不适合修炼",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"压抑": 20, "执念": 15}
                ),
                Choice(
                    id="CH0_CHOICE_09C",
                    text="一定有办法的，一定有",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"执念": 30, "决心": 20}
                )
            ]
        )
    ]
)

# 序章第四段：希望的觉醒
CH0_PHASE_04 = Scene(
    id="CH0_PHASE_04",
    title="雨夜·修炼场",
    description="深夜，暴雨如注。暴雨中的修炼场，积水倒映着主角的身影。主角疯狂挥剑，木剑不断出现裂痕。远处廊下父亲的身影被雨幕模糊。",
    background="rainy_night",
    ambient_sound="environment_heavy-rain",
    events=[
        SceneEvent(
            id="CH0_E10",
            text="【雨夜·修炼场】\n\n深夜，暴雨如注。\n\n你独自来到修炼场，任由雨水打湿衣衫。积水倒映着你模糊的身影。\n\n你开始疯狂挥剑，木剑在雨中不断出现裂痕。\n\n远处廊下，父亲的身影被雨幕模糊，但他没有阻止你。",
            choices=[
                Choice(
                    id="CH0_CHOICE_10A",
                    text="继续疯狂挥剑",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"执念": 30, "愤怒": 15}
                ),
                Choice(
                    id="CH0_CHOICE_10B",
                    text="在雨中怒吼",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"愤怒": 25, "执念": 20}
                ),
                Choice(
                    id="CH0_CHOICE_10C",
                    text="默默承受痛苦",
                    choice_type=ChoiceType.EMOTION,
                    emotion_effects={"压抑": 20, "执念": 25}
                )
            ]
        ),
        SceneEvent(
            id="CH0_E11",
            text="木剑终于断裂了。\n\n\"咔嚓\"一声，木剑在你手中断成两截。\n\n你跪在雨水中，看着断裂的木剑，感到前所未有的绝望。\n\n就在这时，你的脑海中响起一个声音：\n\n【检测到强烈执念，模拟系统启动中...】",
            choices=[
                Choice(
                    id="CH0_CHOICE_11A",
                    text="这是...什么？",
                    choice_type=ChoiceType.SYSTEM,
                    emotion_effects={"执念": 35}
                ),
                Choice(
                    id="CH0_CHOICE_11B",
                    text="幻觉吗？",
                    choice_type=ChoiceType.SYSTEM,
                    emotion_effects={"执念": 30}
                ),
                Choice(
                    id="CH0_CHOICE_11C",
                    text="不管是什么，只要能变强就行",
                    choice_type=ChoiceType.SYSTEM,
                    emotion_effects={"执念": 40, "决心": 25}
                )
            ]
        ),
        SceneEvent(
            id="CH0_E12",
            text="【模拟系统已启动】\n\n【距离魔族入侵还有3年】\n\n【首次模拟可预演未来，积累成长经验】\n\n【时间范围：3年（现实时间消耗：3天）】\n\n【精神力消耗：30点】\n\n你感到一股暖流涌入体内，仿佛看到了改变命运的希望。",
            choices=[
                Choice(
                    id="CH0_CHOICE_12A",
                    text="接受系统，我要变强",
                    choice_type=ChoiceType.SYSTEM,
                    next_scene="CH1_PHASE_01"
                ),
                Choice(
                    id="CH0_CHOICE_12B",
                    text="这是幻觉吗？",
                    choice_type=ChoiceType.SYSTEM,
                    next_scene="CH1_PHASE_01"
                ),
                Choice(
                    id="CH0_CHOICE_12C",
                    text="不管是什么，只要能变强就行",
                    choice_type=ChoiceType.SYSTEM,
                    next_scene="CH1_PHASE_01"
                )
            ]
        )
    ]
)

# 第一章第一段：模拟启动
CH1_PHASE_01 = Scene(
    id="CH1_PHASE_01",
    title="模拟启动·模式选择",
    description="模拟系统启动界面，玩家需要选择模拟模式：激进冒险或见危立逃。",
    background="system_interface",
    ambient_sound="ui_system",
    events=[
        SceneEvent(
            id="CH1_E01",
            text="【首次模拟启动中...】\n\n【时间范围：3年（现实时间消耗：3天）】\n\n【精神力消耗：30点（初始值：100点）】\n\n【请选择模拟模式：】",
            choices=[
                Choice(
                    id="CH1_CHOICE_01A",
                    text="激进冒险：战斗收益+50%，失败死亡率+80%",
                    choice_type=ChoiceType.SYSTEM,
                    emotion_effects={"决心": 20}
                ),
                Choice(
                    id="CH1_CHOICE_01B",
                    text="见危立逃：战斗收益-30%，失败死亡率0%",
                    choice_type=ChoiceType.SYSTEM,
                    emotion_effects={"压抑": 10}
                )
            ]
        ),
        SceneEvent(
            id="CH1_E02",
            text="【模式已确认】\n\n【模拟开始...】\n\n【时间：模拟第3个月】\n\n【场景：演武场】\n\n你再次站在演武场上，但这次，你有了改变命运的机会。",
            choices=[
                Choice(
                    id="CH1_CHOICE_02A",
                    text="开始模拟",
                    choice_type=ChoiceType.SYSTEM,
                    emotion_effects={"决心": 15}
                )
            ]
        )
    ]
)

# 场景数据字典
SCENES = {
    "CH0_PHASE_01": CH0_PHASE_01,
    "CH0_PHASE_02": CH0_PHASE_02,
    "CH0_PHASE_03": CH0_PHASE_03,
    "CH0_PHASE_04": CH0_PHASE_04,
    "CH1_PHASE_01": CH1_PHASE_01,
}

def get_scene(scene_id: str) -> Optional[Scene]:
    """Get scene by ID"""
    return SCENES.get(scene_id)

def get_all_scene_ids() -> List[str]:
    """Get all available scene IDs"""
    return list(SCENES.keys())
