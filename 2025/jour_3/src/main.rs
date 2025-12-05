use std::cmp::max;
use std::cmp::min;
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

fn first_star(value : &str) -> i128{
    let mut maxi : i128 = -1;
    let mut second_maxi : i128 = -1;
    for cur_char in value.chars().rev(){
        if i128::from(cur_char.to_digit(10).unwrap()) >= maxi {
            second_maxi = maxi;
            maxi = i128::from(cur_char.to_digit(10).unwrap());
        }
    }
    if second_maxi == -1{
        let mut first_time = true;
        for cur_char in value.chars().rev(){
            if i128::from(cur_char.to_digit(10).unwrap()) >= maxi {
                if first_time{
                    first_time = false;
                    second_maxi = maxi;
                    maxi = -1;
                    continue;
                }
                second_maxi = max(second_maxi,maxi);
                maxi = i128::from(cur_char.to_digit(10).unwrap());
            }
        }

    }
    return maxi * 10 + second_maxi;
}

fn second_star(value : &str) -> i128{
    let mut vector : Vec<i128> = Vec::new();
    let mut current_char = 0;
    let mut pos_last_char_used = 0;
    while current_char != 12{
        let begin_word = value.split_at(min(value.len() - 12 + pos_last_char_used + 1, value.len()));
        let interesting_part = begin_word.0.split_at(pos_last_char_used).1;
        let mut maxi = 0;
        let mut cur_index = pos_last_char_used;

        if value.len() - cur_index <= 12 - current_char {
            for new_char in value.split_at(cur_index).1.chars(){
                vector.push(i128::from(new_char.to_digit(10).unwrap()));
            }
            break;
        }

        for elem in interesting_part.chars(){
            let tmp = i128::from(elem.to_digit(10).unwrap());
            if tmp > maxi{
                maxi = tmp;
                pos_last_char_used = cur_index + 1;
            }
            if value.len() - cur_index <= 12 - current_char {
                break;
            }
            cur_index += 1;
        }

        vector.push(maxi);
        current_char += 1;
    }
    let mut result : i128 = 0;
    for elem in vector{
        result *= 10;
        result += elem; 
    }
    return result;
}

fn main() {
    let (content, mode) = init();

    let mut result : i128 = 0;
    let split_value = content.split("\n");

    for value in split_value{
        if mode.eq("1"){
            result += first_star(value);
        } else {
            result += second_star(value);
        }
    }
    println!("{result} ");
}
