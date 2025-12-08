use std::env;
use std::fs;
use regex::Regex;
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


fn fun_add(a : i128, b : i128) -> i128{
    a + b
}

fn fun_mult(a : i128, b : i128) -> i128{
    a * b
}

fn first_star(split_value: std::str::Split<'_, &'static str>) -> i128{
    let re = Regex::new(r"\s+").unwrap();
    let mut result = 0;
    let rows = split_value.clone().count();
    let mut cols = 0;
    for tmp_str in re.replace_all(split_value.clone().next().unwrap(), " ").split(" "){
        if tmp_str != ""{
            cols += 1;
        }
    }
    let mut data = vec![vec![0; rows - 1]; cols];
    let mut i = 0;
    for line in split_value{
        let new_line = re.replace_all(&line, " ");
        let mut j = 0;
        let mut current_function : fn(i128, i128) -> i128;
        for number in new_line.split(" "){
            if number.eq(""){
                continue;
            }
            if i + 1 == rows{
                let mut current_value = 0;
                if number.eq("+"){
                    current_function = fun_add;
                } else {
                    assert_eq!(number, "*");
                    current_function = fun_mult;
                    current_value = 1;
                }
                for elem in data[j].iter(){
                    current_value = current_function(current_value, *elem);
                }
                result += current_value;
            } else {
                data[j][i] = number.parse::<i128>().unwrap(); 
            }
            j += 1;
        }
        i += 1;
    }
    result
}


fn main() {
    let (content, mode) = init();

    let mut result : i128 = 0;


    let split_value = content.split("\n");


    if mode.eq("1"){
        result = first_star(split_value);
    } else {
        // result += second_star(matrix);
    }
    println!("result = {}", result);
}
