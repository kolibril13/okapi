
#set page(width: auto, height: auto, margin: 0cm, fill: none)
#set text(size: 80pt)

#let korange() = text(fill: orange)[$k$]
#let nblue() = text(fill: blue)[$n$]

$ sum_(#korange() = 1)^#nblue() #korange() = (nblue()(nblue()+1)) / 2 $  
