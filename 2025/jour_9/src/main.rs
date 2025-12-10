use std::collections::HashMap;
use std::env;
use std::fs;
use std::cell::RefCell;

thread_local!(static DEBUG: RefCell<bool> = RefCell::new(true));

#[derive(Debug, Clone, Copy)]
struct Tile{
    line : i128,
    column : i128,
}

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

fn create_tile(matrix: & Vec<String>) -> Vec<Tile> {
    let mut result : Vec<Tile> = Vec::new();
    let mut i = 0;
    for line in matrix{
        if line.eq(""){
            continue;
        }
        let mut values = line.split(",");
        let x = values.next().unwrap().parse::<i128>().unwrap();
        let y = values.next().unwrap().parse::<i128>().unwrap();
        result.push(Tile{line : y, column : x});
        i += 1;
    }
    return result;

}


fn first_star(matrix : Vec<String>) -> i128{
    let vec_tile = create_tile(&matrix);
    let matrix_dist = create_matrix_dist(&vec_tile);

    let (elem_1, elem_2) = get_pair_with_max_distance(&matrix_dist);

    println!("elem_1 : {:?}, elem_2 : {:?}", vec_tile[elem_1], vec_tile[elem_2]);
    brute_force(matrix);

    return size_rectangle(vec_tile[elem_1], vec_tile[elem_2]);
}

fn brute_force(matrix : Vec<String>){
    let vec_tile = create_tile(&matrix);
    let mut maxi = -1;
    let mut good_1 = &vec_tile[0];
    let mut good_2 = &vec_tile[0];

    for elem in &vec_tile{
        for elem_2 in &vec_tile{
            let a = size_rectangle(*elem, *elem_2); 
            if a > maxi{
                maxi = a;
                good_1 = elem;
                good_2 = elem_2;
            }
        }
    }
    println!("distance max = {} sur elem_1 = {:?}, eleme_2 = {:?}", maxi, good_1, good_2);

}

fn size_rectangle(elem_1: Tile, elem_2: Tile) -> i128 {
    return ((elem_1.line - elem_2.line).abs() + 1) * (( elem_1.column - elem_2.column).abs() + 1);
}



fn second_star(matrix : Vec<String>) -> i128{
    println!("{:?}", matrix);
    0
}

fn get_pair_with_max_distance(matrix_dist: &Vec<Vec<i128>>) -> (usize, usize) {
    let mut result_line = 0;
    let mut result_column = 1;
    let mut maxi = -1; 
    for (line, content) in matrix_dist.iter().enumerate(){
        for (column, dist) in content.iter().enumerate(){ // la matrice sera toujours symétrique ->
                                                          // on peut couper en deux
            if line.le(&column){
                continue;
            }
            if *dist > maxi {
                maxi = *dist; 
                result_line = line;
                result_column = column;
            }
        }
    }
    println!("maxi  =  {}", maxi);
    return (result_line, result_column);
}

fn create_matrix_dist(vec_tile: &Vec<Tile>) -> Vec<Vec<i128>> {
    let mut result : Vec<Vec<i128>> = Vec::new();
    for (i, elem_1) in vec_tile.iter().enumerate(){
        result.push(Vec::new());
        for elem_2 in vec_tile.iter(){
            result[i].push(get_distance(elem_1, elem_2));
        }
    }

    return result;

}

fn get_distance(elem_1: &Tile, elem_2: &Tile) -> i128 {
    return (elem_1.line - elem_2.line).pow(2) + (elem_1.column - elem_2.column).pow(2);
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
