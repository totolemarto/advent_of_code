use std::env;
use std::fs;

fn main() {
    let args: Vec<String> = env::args().collect();
    let file_name = &args[1];
    let contenu = fs::read_to_string(file_name)
        .expect("Quelque chose s'est mal passé lors de la lecture du fichier");
    let mut current : i32 = 50;
    let mut result : i32 = 0;
    let split_value = contenu.split("\n");
    for value in split_value{
        if value.len() < 1{
            break;
        }
        println!("{value} {current}");
        let numberstr = &value[1..];
        let offset : i32 = numberstr.parse::<i32>().unwrap();
        if value.starts_with("L"){

            current -= offset;

        } else {
            current += offset;
        }
        while current < 0 || current > 99{
            if current > 99 {
                current = current % 100;
            }
            if current < 0{
                current += 100;
            }
        }
        if current == 0{
            result += 1;
        }
    }
    
    println!("{result} ");
}
