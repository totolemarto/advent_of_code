use std::env;
use cast::{i128};
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

fn get_index_end(last_line : &str) -> Vec<usize>{
    let mut vector : Vec<usize> = vec![];
    for (i, charac) in last_line.chars().enumerate(){
        if charac.eq(&'+') || charac.eq(&'*'){
            vector.push(i);
        }
    }
    vector
}

fn create_number(new_value_vec: &Vec<&str>, rows: usize, cols: usize) -> Vec<Vec<i128>> {
    let mut data = vec![vec![0; rows]; cols];
    let last_line = new_value_vec.last().unwrap(); 
    let index_end = get_index_end(last_line);
    let mut current_column = 0;
    let mut current_line = 0;
    for j in 0..new_value_vec.get(0).unwrap().len(){
        if index_end.contains(&j) && j != 0{
            current_line += 1;
            current_column = 0;
        }
        for i in 0..rows-1{
            let charac = new_value_vec.get(i).unwrap().chars().nth(j).unwrap();
            if charac.eq(&' '){
                continue;
            }
            let value = i128(charac.to_digit(10).unwrap());
            data[current_line][current_column] = data[current_line][current_column] * 10 + value;
        }
        current_column += 1;
    }
    data
}

fn second_star(split_value: &Vec<&str>) -> i128{
    let re = Regex::new(r"\s+").unwrap();
    let mut result = 0;
    let rows = split_value.len();
    let mut cols = 0;
    for tmp_str in re.replace_all(split_value.get(0).unwrap(), " ").split(" "){
        if tmp_str != ""{
            cols += 1;
        }
    }
    let data = create_number(&split_value, rows, cols);
    let last_line = split_value.last().unwrap(); 
    let mut current_function : fn(i128, i128) -> i128;
    let mut current_column = 0;
    for number in last_line.chars(){
        if number.eq(&' '){
            continue;
        }
        let mut current_value = 0;
        if number.eq(&'+'){
            current_function = fun_add;
        } else {
            current_function = fun_mult;
            current_value = 1;
        }
        for i in 0..rows - 1{
            if data[current_column][i] == 0{
                continue;
            }
            current_value = current_function(current_value, data[current_column][i]);

        }
        current_column += 1;
        result += current_value;
    }
    result
}



fn main() {
    let (content, mode) = init();

    let result : i128;


    let split_value = content.split("\n");


    if mode.eq("1"){
        result = first_star(split_value);
    } else {
        result = second_star(&split_value.collect());
    }
    println!("result = {}", result);
}
