use std::env;
use std::fs;

fn init() -> (String, String) {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3{
        println!("usage <file to read> < step for stars>");
        std::process::exit(1);
    }

    let file_name = &args[1];
    let mode = &args[2];
    let mut content = fs::read_to_string(file_name)
        .expect("Error while reading file");

    content.pop(); // remove 0x0a from content
    (content, mode.clone())
}

fn first_star(i : i128) -> i128{
    let str_repr = i.to_string();
    if str_repr.len() % 2 != 0{
        return 0;
    }
    let two_parts = str_repr.split_at(str_repr.len() / 2);
    if two_parts.0.eq(two_parts.1){
        return i;
    }
    return 0;
}

fn second_star(i : i128) -> i128{
    let str_repr = i.to_string();
    for j in 0..str_repr.len() / 2 + 1{
        let current_sub_string = str_repr.split_at(j);
        if str_repr.matches(current_sub_string.0).count() * current_sub_string.0.len() == str_repr.len(){
            return i;
        }
    }
    return 0;
}

fn main() {
    let (content, mode) = init();

    let mut result : i128 = 0;
    let split_value = content.split(",");

    for value in split_value{
        if value.len() < 1{
            break;
        }
        let mut bornes = value.split("-");
        let inf_borne = bornes.next().unwrap().parse::<i128>().unwrap();
        let sup_borne = bornes.next().unwrap().parse::<i128>().unwrap();
        for i in inf_borne..sup_borne + 1{
            if mode.eq("1"){
                result += first_star(i);
            } else {
                result += second_star(i);
            }
        }
    }
    println!("{result} ");
}
