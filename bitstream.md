# Bitstream

```json
{
    "layout": [
        [],
        []
    ],
    "inputs": [

    ],
    "outputs": [

    ],
    "luts": [
        {

        }
    ]
}

```

Example
```json
{
    "layout": [
        [
            ["lut1_a","rd","lut2"],
            ["0",     "rd","lut2"],
            ["lut1_b","r", "0"]
        ],
        [
            ["0", "rd","0"],
            ["o1","rd","0"],
            ["0", "r", "0"]
        ]
    ],
    "wire": [
        [
            [
                [0,0], [0,1]
            ],
            [
                [0,1], [1,1]
            ],
            [
                [1,1], [2,1]
            ],
            [
                [1,3], [2,3]
            ]
        ],
        []
    ],
    "input": [
        [
            "a", [0,0,0] // [var, [layout stage, x, y]]
        ],
        [
            "b", [0,0,3]
        ]
    ],
    "output": [
        [
            [
                "o1", [1,0,0]
            ]
        ]
    ],
    "luts": [
        {
            "name": "lut1",
            "type": 4, // or 6,
            "op": "and",
            "location": [0,0], // [layout stage, x]
            "connections": [
                [
                    [0,0],
                    [0,2]
                ]
            ]
        },
        {
            "name": "lut2",
            "type": 4,
            "op": "or",
            "location": [0,2],
            "connections": [
                [
                    [0,0],
                    [0,1]
                ]
            ]
        }
    ]
}
```

