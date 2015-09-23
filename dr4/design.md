# Orion
## Stickbug
Goal: Generate simplified robot geometries, to analyze for gaits robustness & efficiency
Each robot is described as a tree, consisting of links (rigid members of a determined orientation and length) and motors, consisting of a rotation axis (described by a direction)
Each link/motor has a single connection point, to which multiple members can be attached.
Example structure:
[root
  children:[
    [motor
      direction:(3.14,0.0)
      children:[
        [link
          children:[]
        ]
      ]
    ]
    [link
      direction:()
    ]
  ]
]
