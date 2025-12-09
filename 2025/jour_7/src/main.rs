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

fn put_tachyon(line : usize, column : usize, matrix :  &mut [String]) -> i32{
    if line >= matrix.len() || column >= matrix.get(0).unwrap().len(){
        return 0;
    }
    if matrix.get(line).unwrap().chars().nth(column).unwrap() == '.'{
        let mut new_line = matrix.get_mut(line).unwrap().to_string();
        new_line.replace_range(column..column + 1, "|");
        matrix[line] = new_line;
        return 0;
    }
    if matrix.get(line).unwrap().chars().nth(column).unwrap() == '^'{
        let tmp = put_tachyon(line, column - 1, matrix);
        return  1 + put_tachyon(line, column + 1, matrix) + tmp;
    }
    return 0;
}

fn iteration(matrix : &mut [String], min_line : usize, max_line : usize) -> i32{
    let mut result = 0;
    for line in min_line..max_line {
        for column in 0..matrix.get(0).unwrap().len(){
            if matrix.get(line).unwrap().chars().nth(column).unwrap() == '|'{
                result += put_tachyon(line + 1, column, matrix);
            } else if matrix.get(line).unwrap().chars().nth(column).unwrap() == 'S'{ 
                result += put_tachyon(line + 1, column, matrix);
            }             
        }
    }
    return result;
}
fn first_star(matrix : &mut [String]) -> i32{
    let mut line_begin = 0;
    let mut cur_add ;
    let mut result = 0;
    while line_begin < matrix.len() - 1{ 
        cur_add = iteration(matrix, line_begin, line_begin + 1);
        //println!("ligne = {} -> result tmp = {}", line_begin, cur_add);
        line_begin += 1;
        result += cur_add;
    }
    for line in matrix{
        println!("{}", line);
    }
    return result;
}

fn second_star(split_value: &[String]) -> i32{
    return 0;
}



fn main() {
    let (content, mode) = init();

    let result : i32;


    let mut split_value: Vec<String> = content.split("\n").map(|s| s.to_string()).collect();



    if mode.eq("1"){
        result = first_star(&mut split_value);
    } else {
        result = second_star(&split_value);
    }
    println!("result = {}", result);
}
