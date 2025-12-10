use std::cmp::Ordering;
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


#[derive(Debug, Clone, Copy)]
struct Tile{
    line : i128,
    column : i128,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Copy)]
struct Rectangle{
    corner_1 : Tile,
    corner_2 : Tile,
    area : i128,
}
impl Eq for Rectangle{
}
impl PartialEq for Rectangle{
    fn eq(&self, other : &Self) -> bool{
        return self.area == other.area;
    }
}

impl Ord for Rectangle {
    fn cmp(&self, other: &Self) -> Ordering {
        other.area.cmp(&self.area)
    }
}

impl PartialOrd for Rectangle{
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(other.area.cmp(&self.area))
    }
}
fn create_tile(matrix: & Vec<String>) -> Vec<Tile> {
    let mut result : Vec<Tile> = Vec::new();
    for line in matrix{
        if line.eq(""){
            continue;
        }
        let mut values = line.split(",");
        let x = values.next().unwrap().parse::<i128>().unwrap();
        let y = values.next().unwrap().parse::<i128>().unwrap();
        result.push(Tile{line : y, column : x});
    }
    return result;

}


fn first_star(matrix : Vec<String>) -> i128{
    return create_rectangle_vector(matrix).iter().next().unwrap().area;
}

fn size_rectangle(elem_1: Tile, elem_2: Tile) -> i128 {
    return ((elem_1.line - elem_2.line).abs() + 1) * (( elem_1.column - elem_2.column).abs() + 1);
}



fn second_star(matrix : Vec<String>) -> i128{
    println!("{:?}", matrix);
    0
}

// fn create_matrix_area(vec_tile: &Vec<Tile>) -> Vec<Vec<i128>> {
//     let mut result : Vec<Vec<i128>> = Vec::new();
//     for (i, elem_1) in vec_tile.iter().enumerate(){
//         result.push(Vec::new());
//         for j in i + 1..vec_tile.len(){
//             result[i].push(size_rectangle(*elem_1, vec_tile[j]));
//         }
//     }
//
//     return result;
//
// }

fn create_rectangle_vector(matrix : Vec<String>) -> Vec<Rectangle>{
    let vec_tile = create_tile(&matrix);
    let mut result : Vec<Rectangle> = Vec::new();
    for i in 0..vec_tile.len(){
        for j in i + 1..vec_tile.len(){
            result.push(Rectangle{corner_1 : vec_tile[i], corner_2 : vec_tile[j], area : size_rectangle(vec_tile[i], vec_tile[j])});
        }
    }
    result.sort();
    result
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
// input -> 1227
