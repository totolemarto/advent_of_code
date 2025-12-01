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
    let content = fs::read_to_string(file_name)
        .expect("Error while reading file");

    (content, mode.clone())
}

fn main() {
    let (content, mode) = init();

    let mut current : i32 = 50;
    let mut result : i32 = 0;
    let split_value = content.split("\n");

    for value in split_value{
        if value.len() < 1{
            break;
        }
        let numberstr = &value[1..];
        let offset : i32 = numberstr.parse::<i32>().unwrap();
        let mut skip = current == 0;

        current += if value.starts_with("L") {-offset} else {offset};

        while current < 0 || current > 99{
            if current > 99 {
                if mode.eq("2") {
                    result += current / 100;
                }
                current = current % 100;
                if current == 0{
                    result -= 1;
                }
            }
            if current < 0{
                if mode.eq("2") &&  !skip {
                    result += 1;
                }
                current += 100;
            }
            skip = false;
        }
        result += if current == 0 {1} else {0};
    }
    println!("{result} ");
}
