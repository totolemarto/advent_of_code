use std::cmp::max;
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
    // let str_repr = i.to_string();
    // let total_len = str_repr.len();
    // for j in 1..str_repr.len() / 2 + 1{
    //     let current_sub_string = str_repr.split_at(j);
    //     if str_repr.matches(current_sub_string.0).count() * j == total_len{
    //         return i;
    //     }
    // }
    return 0;
}

fn main() {
    let (content, mode) = init();

    let mut result : i128 = 0;
    let split_value = content.split("\n");

    for value in split_value{
        if mode.eq("1"){
            result += first_star(value);
        } else {
            // result += second_star(value);
        }
    }
    println!("{result} ");
}
