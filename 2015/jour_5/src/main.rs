use std::env;
use std::fs;
use std::collections::HashMap;

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

fn analyze_word(line: &str) -> i32 {
    let vowels = "aeiou";
    let mut cur_vow = 0;
    let mut repeat = false;
    let mut prev_char = '1';
    for charac in line.chars() {
        if vowels.contains(charac){
            cur_vow += 1;
        }
        if charac.eq(&prev_char){
            repeat = true;
        }
        if      charac == 'b' && prev_char == 'a'
            ||  charac == 'd' && prev_char == 'c'
            ||  charac == 'q' && prev_char == 'p'
            ||  charac == 'y' && prev_char == 'x'
        {
            return 0;
        }

        prev_char = charac;
    }

    if cur_vow >= 3 && repeat {
        return 1;
    }
    return 0;
}

fn analyze_word_part_2(line: &str) -> i32 {
    let mut couple_letter: HashMap<String, usize> = HashMap::new();
    let mut double = false;
    let mut good = false;
    for (i, charac) in line.chars().enumerate() {
        if i == 0{
            continue;
        }
        double = double || ( i > 1 && line.chars().nth(i - 2).unwrap() == charac);
        let cur_key: String = vec![line.chars().nth(i-1).unwrap(), charac].into_iter().collect();
        if couple_letter.contains_key(&cur_key){ 
            good = good || couple_letter[&cur_key] + 1 != i;
        } else {
            couple_letter.insert(cur_key, i); 
        }
    }
    return if double && good {1} else {0};
}

fn main() {
    let (content, mode) = init();
    let lines = content.split("\n");
    let mut result = 0;
    for line in lines{
        if mode.eq("1"){
            result += analyze_word(line);
        } else{
            result += analyze_word_part_2(line);
        }
    }
    println!("{}", result);
}
