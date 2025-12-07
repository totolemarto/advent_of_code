use std::env;
use std::fs;
use std::cell::RefCell;

thread_local!(static DEBUG: RefCell<bool> = RefCell::new(true));

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
    let split_value = content.split("\n");

    let mut data = false;
    let mut vec_range : Vec<(i128, i128)> = vec![];
    for line in split_value{
        if line.eq(""){
            data = true;
            continue
        }
        if ! data{
            let mut two_values = line.split("-");

            let begin = two_values.next().unwrap().parse::<i128>().unwrap();
            let end = two_values.next().unwrap().parse::<i128>().unwrap();
            vec_range.push((begin,end));

        } else {
            if mode.eq("1"){
                let current = line.parse::<i128>().unwrap();
                for bounds in vec_range.iter(){
                    if bounds.0 <= current && current <= bounds.1{
                        result += 1;
                        break;
                    }
                }

            } else {
                // result += second_star(matrix);
            }
        }
    }
    println!("{result} ");
}
