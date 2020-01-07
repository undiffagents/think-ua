
OWL_INSTRUCTIONS = [
    'task(Psychomotor-Vigilance)',
    'button(Acknowledge)',
    'box(Box)',
    'target(Target)',
    'letter(Letter)',
    'subject(Subject)',
    'isPartOf(Box,Psychomotor-Vigilance)',
    'isPartOf(Target,Psychomotor-Vigilance)',
    'isPartOf(Letter,Target)',
    # 'hasProperty(Psychomotor-Vigilance,active)=>appearsIn(Target,Box)',
    'appearsIn(Target,Box)=>click(Subject,Acknowledge),remember(Subject,Letter)',
    'done(Psychomotor-Vigilance)'
]
