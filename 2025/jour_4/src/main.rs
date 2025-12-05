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


#[derive(Debug, Clone)]
struct Matrix {
    rows: usize,
    cols: usize,
    data: Vec<Vec<usize>>,
}


fn is_accessible(value : &Matrix, i : usize, j : usize) -> bool{
    let mut result = 0;
    if i > 0{
        result += value.data[i-1][j];
    }
    if i + 1 < value.rows{
        result += value.data[i+1][j];
    }
    if j > 0{
        result += value.data[i][j-1];
    }
    if j + 1 < value.cols{
        result += value.data[i][j + 1];
    }
    if i > 0 && j > 0{
        result += value.data[i-1][j - 1];
    }
    if i > 0 && j + 1 < value.cols{
        result += value.data[i-1][j + 1];
    }
    if i + 1 < value.rows && j > 0{
        result += value.data[i+1][j - 1];
    }
    if i + 1 < value.rows && j + 1 < value.cols {
        result += value.data[i+1][j+1];
    }

    return result < 4;
}

fn first_star(matrix : Matrix) -> i128{
    let mut data = vec![vec!['.'; matrix.cols]; matrix.rows];


    let mut result = 0;
    for i in 0..matrix.clone().rows{
        for j in 0..matrix.clone().cols{
            if matrix.data[i][j] != 1{
                continue;
            }
            let tmp = if is_accessible(&matrix, i, j) {1} else {0};
            data[i][j] = if matrix.data[i][j] == 1 && tmp == 1 {'x'} else if matrix.data[i][j] == 1 {'@'} else {'.'};
            result += tmp;
            assert_eq!(tmp == 1, data[i][j] == 'x');
        }
    }
    // for line in data.clone(){
    //     println!("{:?}", line);
    // }
    // println!("{} ", result);
    return result;
}

fn second_star(mut matrix : Matrix) -> i128{
    let mut data = vec![vec!['.'; matrix.cols]; matrix.rows];


    let mut result = 0;
    let mut prev_value = 1;
    let mut current_value;
    while result != prev_value {
        current_value = 0;
        for i in 0..matrix.clone().rows{
            for j in 0..matrix.clone().cols{
                if matrix.data[i][j] != 1{
                    continue;
                }
                let tmp = if is_accessible(&matrix, i, j) {1} else {0};
                data[i][j] = if matrix.data[i][j] == 1 && tmp == 1 {'x'} else if matrix.data[i][j] == 1 {'@'} else {'.'};
                current_value += tmp;
                assert_eq!(tmp == 1, data[i][j] == 'x');
            }
        }
        for i in 0..matrix.clone().rows{
            for j in 0..matrix.clone().cols{
                if data[i][j] == 'x'{
                    matrix.data[i][j] = 0;
                    data[i][j] = '.';
                }
            }
        }
        prev_value = result;
        result += current_value;
    }
    // for line in data.clone(){
    //     println!("{:?}", line);
    // }
    // println!("{} ", result);
    return result;
}

fn main() {
    let (content, mode) = init();

    let mut result : i128 = 0;
    let split_value = content.split("\n");
    let rows = split_value.clone().next().unwrap().len();
    let cols = split_value.clone().count();
    let mut data = vec![vec![0; cols]; rows];


    let mut i = 0;
    for line in split_value{
        let mut j = 0;
        for charac in line.chars(){
            data[i][j] = if charac == '@' {1} else {0};
            j += 1;
        }
        i += 1;
    }
    let matrix : Matrix = Matrix { rows, cols, data};
    if mode.eq("1"){
        result = first_star(matrix);
    } else {
        result += second_star(matrix);
    }
    println!("{result} ");
}
