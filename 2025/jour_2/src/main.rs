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

fn main() {
    let (content, mode) = init();

    let mut result : i128 = 0;
    let split_value = content.split(",");

    for value in split_value{
        println!("value = {} ", value);
        if value.len() < 1{
            break;
        }
        let mut bornes = value.split("-");
        let inf_borne = bornes.next().unwrap().parse::<i128>().unwrap();
        let sup_borne = bornes.next().unwrap().parse::<i128>().unwrap();
        println!("inf = {} sup = {}", inf_borne, sup_borne);
        for i in inf_borne..sup_borne + 1{
            let str_repr = i.to_string();
            if str_repr.len() % 2 != 0{
                continue;
            }
            let first_part = str_repr.split_at(str_repr.len() / 2);
            if first_part.0.eq(first_part.1){
                result += i;
            }
        }
        if mode.eq("2"){
            println!("coucou");
        }

    }
    println!("{result} ");
}
