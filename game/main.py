from assets import scores
from assets import roller
from assets import engine


# build a new engine
e = engine.Engine()

while True:
    val = input("# ")

    match val:
        case "exit":
            break
        case "quit":
            break
        case "score":
            e.print_grand_total()
        case "roll":
            e.round()
        case "end":
            e.end_turn()
        case _:
            try:
                e.save_choices(val)
            except Exception as ex:
                print("That is not a valid choice")








