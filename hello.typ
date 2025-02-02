
#let group-counter = counter("groups")

#let group(it, name: none) = {
  let labelled(x, y)=[#x #y]

  if type(name) == type("") {
    return labelled(box[#it], label(name));
  }

    group-counter.step()
  context{
    let group-name = "Group " + str(group-counter.get().at(0) -1);
    return labelled(box[#it], label(group-name));
  }
}

#group(name: "4")[dcd]
#group[dddddd]

#group[dddddd]

$
  group(x) = 1
$
