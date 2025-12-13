use std::env;
use std::fs;

const DEBUG : bool = false;

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
struct Machine{
    lights : Vec<bool>,
    buttons : Vec<Vec<usize>>,
    joltage : Vec<u32>,
    cur_light : Vec<bool>,
}

fn create_machines(matrix: & Vec<String>) -> Vec<Machine> {
    let mut result : Vec<Machine> = Vec::new();
    for line in matrix{
        if line.eq(""){
            continue;
        }
        let lights = get_lights(line);
        let buttons = get_buttons(line);
        let joltage = get_joltage(line);
        let cur_light = vec![false; lights.len() ];
        result.push(Machine{ lights, buttons, joltage, cur_light});
    }
    return result;
}

fn get_joltage(line: &str) -> Vec<u32> {
    let mut result : Vec<u32> = Vec::new();
    let characs :Vec<char> = line.chars().collect();
    let mut i = 1;
    while i < line.len(){
        if characs.get(i).unwrap() == &'{'{
            let mut new_one = true;
            while  characs.get(i).unwrap() != &'}'{
                let value = characs.get(i).unwrap();
                if value.is_digit(10){
                    if new_one{
                        result.push(value.to_digit(10).unwrap());
                        new_one = false;
                    } else{
                        let size = result.len() - 1;
                        *result.get_mut(size).unwrap() = *result.get_mut(size).unwrap() * 10 + value.to_digit(10).unwrap() ;
                    }
                } else{ // une ,
                    new_one = true;
                }
                i += 1;
            }
            i -= 1;
        }
        i += 1;
    }
    result
}

fn get_buttons(line: &str) -> Vec<Vec<usize>> {
    let mut result : Vec<Vec<usize>> = Vec::new();
    let characs :Vec<char> = line.chars().collect();
    let mut i = 1;
    while i < line.len(){
        if characs.get(i).unwrap() == &'{'{
            return result;
        }
        if characs.get(i).unwrap() == &'('{
            let mut button = Vec::new();
            let mut new_one = true;
            i += 1;
            while  characs.get(i).unwrap() != &')'{
                let value = characs.get(i).unwrap();
                if value.is_digit(10){
                    if new_one{
                        button.push(value.to_digit(10).unwrap() as usize);
                        new_one = false;
                    } else{
                        let size = button.len() - 1;
                        *button.get_mut(size).unwrap() = *button.get_mut(size).unwrap() * 10 + value.to_digit(10).unwrap() as usize;
                    }
                } else{ // une ,
                    assert_eq!(value, &',');
                    new_one = true;
                }
                i += 1;
            }
            i -= 1;
            result.push(button);
        }
        i += 1;
    }
    result
}

fn get_lights(line: &str) -> Vec<bool> {
    let mut result : Vec<bool> = Vec::new();
    let characs :Vec<char> = line.chars().collect();
    for i in 1..line.len(){
        if characs.get(i).unwrap() == &']'{
            return result;
        }
        if characs.get(i).unwrap() == &'.'{
            result.push(false);
        }
        if characs.get(i).unwrap() == &'#'{
            result.push(true);
        }
    }
    result
}


fn first_star(matrix : Vec<String>) -> i128{
    let vec_machines = create_machines(&matrix);
    if DEBUG{
        println!("voici les machines : ");
        for machine in &vec_machines{
            println!("{:?}", machine);
        }
    }
    // toutes les machines doivent avoir même état que leur vecteur et commencent avec tout
    // interrupteur a faux

    let mut result : i128 = 0;
    for machine in &vec_machines{
        result += get_fewest_buttons(&machine, 0, 0);
    }
    result
}

fn get_fewest_buttons(machine: &Machine, cur_button : usize, cur_value : i128) -> i128{
//    println!("on est sur {:?} avec value = {} et nb_button = {}", machine, cur_value, cur_button);
    // version ou le bouton est éteint
    if cur_button >= machine.buttons.len(){
        for i in 0..machine.lights.len(){
            if machine.lights.get(i).unwrap() != machine.cur_light.get(i).unwrap(){
                return 9999999999999999;
            }
        }
        return cur_value;
    }
    let tmp = get_fewest_buttons(&machine.clone(), cur_button + 1, cur_value);


    let mut new_machine = machine.clone();
    for elem in machine.buttons.get(cur_button).unwrap(){
        *new_machine.cur_light.get_mut(*elem).unwrap() = ! machine.cur_light.get(*elem).unwrap();
    }

    // version ou bouton est activé 
    //

    let tmp2 = get_fewest_buttons(&new_machine, cur_button + 1, cur_value + 1);
    if tmp2 == 0{
        return tmp;
    }
    
    return tmp.min(tmp2);
}

fn second_star(matrix : Vec<String>) -> i128{
    -1
}

fn main() {
    let (content, mode) = init();

    let result : i128;


    let split_value: Vec<String> = content.split("\n").map(|s| s.to_string()).collect();


    if mode.eq("1"){
        result = first_star(split_value);
    } else {
        result = second_star(split_value);
    }
    println!("result = {}", result);
}
