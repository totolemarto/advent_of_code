use std::env;
use std::fs;
use std::cell::RefCell;
use std::slice::Iter;

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
/*
 * bounds                |                           |
 *
 * cas 1                    |               |                   ( full inside )
 *
 * cas 2                                                |           |  ( full outside )
 *
 * cas 3       |   |                                                   ( full outside)
 *
 * cas 4            |                                      |           ( part inside )
 *
 * cas 5                        |                           |          ( begin part inside )
 *
 * cas 6        |                   |                                  ( end part inside )
 *
 */
fn second_part(begin : i128, end : i128, vector : &Vec<(i128, i128)>) -> i128 {
    for bounds in vector.iter(){
        if bounds.0 <= begin && end <= bounds.1{ // cas 1
            return 0;
        }
        if bounds.1 < begin { // cas 2
        }
        if bounds.0 > end{ // cas 3
        }
        if bounds.0 >= begin && bounds.1 <= end { // cas 4
            return second_part( begin , bounds.0 - 1, vector) + second_part(bounds.1 + 1 , end, vector);
        }
        if bounds.0 <= begin && begin <= bounds.1 && bounds.1 <= end{ // cas 5
            return second_part(begin, bounds.1 - 1, vector) + second_part(bounds.1 + 1, end, vector);
        }
        if bounds.0 >= begin && bounds.0 <= end && end <= bounds.1 { // cas 6
            return second_part(begin, bounds.0 - 1, vector) + second_part(bounds.0 + 1, end, vector);
        }
    }

    return end - begin + 1;
}

fn first_part(current : i128, vector : Iter<(i128, i128)>) -> i128 {
    for bounds in vector{
        if bounds.0 <= current && current <= bounds.1{
            return 1;
        }
    }
    0
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
            let mut tmp = 0;
            if mode.eq("2"){
                tmp = second_part(begin, end, &vec_range);
            }
            vec_range.push((begin,end));
            result += tmp;
        } else {
            if mode.ne("1"){
                continue;
            }
            let current = line.parse::<i128>().unwrap();
            result += first_part(current, vec_range.iter());
        }
    }
    println!("{result} ");
}
// 367425856150254 -> too hight
