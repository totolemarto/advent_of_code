use std::cmp::Ordering;
use std::collections::HashMap;
use std::env;
use std::fs;

const DEBUG : bool = false ;

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
    let vec_tile = create_tile(&matrix);
    return create_rectangle_vector(&vec_tile).iter().next().unwrap().area;
}

fn create_rectangle_vector(vec_tile : &Vec<Tile>) -> Vec<Rectangle>{
    let mut result : Vec<Rectangle> = Vec::new();
    for i in 0..vec_tile.len(){
        for j in i + 1..vec_tile.len(){
            result.push(Rectangle{corner_1 : vec_tile[i], corner_2 : vec_tile[j], area : size_rectangle(vec_tile[i], vec_tile[j])});
        }
    }
    result.sort();
    result
}

fn size_rectangle(elem_1: Tile, elem_2: Tile) -> i128 {
    return ((elem_1.line - elem_2.line).abs() + 1) * (( elem_1.column - elem_2.column).abs() + 1);
}

fn show_zone(nb_line : i128, nb_cols : i128, valid_zone: &HashMap<i128, Vec<(i128, i128)>>){
    for i in 0..nb_line{
        for j in 0..nb_cols{
            if valid_zone.contains_key(&i){
                let mut good =false;
                for elem in valid_zone.get(&i).unwrap(){
                    if elem.0 <= j && elem.1 >= j{
                        print!("X");
                        good = true;
                        break;
                    }
                }
                if good{
                    continue;
                }
            }
            print!(".");
        }
        println!();
    }

}


fn second_star(matrix : Vec<String>) -> i128{
    let vec_tile = create_tile(&matrix);
    let vec_rectangle = create_rectangle_vector(&vec_tile);
    let mut valid_zone = get_zone(&vec_tile);
    let mut zones : Vec<&i128> = valid_zone.keys().collect();
    zones.sort();
    sort_zone(&mut valid_zone);
    fill_zone(& mut valid_zone);
    sort_zone(&mut valid_zone);
    fill_zone(& mut valid_zone);
    // show_zone(10, 13, &valid_zone);
    let mut zones2 : Vec<&i128> = valid_zone.keys().collect();
    zones2.sort();
    // for key in zones2.clone(){
    //     println!("ligne {} : {:?}", key, valid_zone.get(&key).unwrap());
    // }
    // let mut degage = 0;
    let mut memory : HashMap<(i128, i128), i128> = HashMap::new();
    for rectangle in vec_rectangle.clone(){
        // degage += 1;
        // println!("on en dégage {} sur {}", degage, vec_rectangle.clone().len());
        // println!("on tente sur le rectangle :{:?}", rectangle);

        if is_valid_rectangle(rectangle, &valid_zone, &mut memory){
            println!("on sort sur le rectangle :{:?}", rectangle);
            return rectangle.area;
        }
    }
    -1
}

fn sort_zone(valid_zone: &mut HashMap<i128, Vec<(i128, i128)>>) {
    for values in valid_zone.values_mut(){
        values.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap());
        let mut i = 0;
        while i < values.len() - 1{
            if values[i].0 == values[i].1 && values[i].0 == values[i + 1].0{
                values.remove(i);
                i -= 1;
            }
            if  i > 0 && values[i].0 == values[i].1 && values[i].0 == values[i - 1].1{
                values.remove(i);
                i -= 1;
            }
            i += 1;
        }
        // println!("va t'on supprimer le dernier ? {:?}", values);
        if values[values.len() - 1].0 == values[values.len() - 1]. 1 && values.len() >= 2 && values[values.len() - 2].1 == values[values.len() -1].0{
            values.remove(values.len() -1);
        }
    }
}

fn fill_zone(valid_zone: &mut HashMap<i128, Vec<(i128, i128)>>) {
    for keys in valid_zone.clone().keys(){
        let vector = valid_zone.get_mut(keys).unwrap();
        for i in 0..vector.len() - 1 {
            if i % 2 == 1 && vector[i].0 == vector[i].1 {
                continue;
            }
            if i + 1 < vector.len() && ( ! ( vector[i].0 != vector[i].1 && vector[i +1].0 != vector[i+1].1)){
                vector[i].1 = vector[i + 1].1;
            }

        }
    }
}

fn is_valid_rectangle(rectangle: Rectangle, valid_zone: &HashMap<i128, Vec<(i128, i128)>>, memory : &mut HashMap<(i128, i128), i128>) -> bool {
    for line in rectangle.corner_1.line.min(rectangle.corner_2.line)..rectangle.corner_1.line.max(rectangle.corner_2.line){
        let mut col = rectangle.corner_1.column.min(rectangle.corner_2.column) + 1;
        if !valid_zone.contains_key(&line){
            return false;
        }
        loop{
            let increment = col_is_inside_more(col, line, &valid_zone, memory);
            if increment == -1{
                if DEBUG{
                    println!("c'est perdu pour le rectangle {:?} à cur_col = {} sur line = {}", rectangle, col, line);
                }
                return false;
            }
            if  col >= rectangle.corner_1.column.max(rectangle.corner_2.column){
                break;
            }
            if col == increment{
                col += 1;
                continue;
            }
            col = increment;
        }
    }
    true
}


fn get_zone(vec_tile: &Vec<Tile>) -> HashMap<i128, Vec<(i128, i128)>>{
    let mut result : HashMap<i128 , Vec<(i128, i128)>> = HashMap::new();
    for i in 0..vec_tile.len(){
        let other;
        if i == 0{
            other = vec_tile.len() - 1;
        } else{
            other = i-1;
        }
        if vec_tile[i].line == vec_tile[other].line{
            add_range_in_line(vec_tile[i].line, vec_tile[i].column, vec_tile[other].column, &mut result);
        } else{
            add_range_in_column(vec_tile[i].column, vec_tile[i].line, vec_tile[other].line, &mut result);

        }
    }
    result
}


fn col_is_inside_more(column : i128, line : i128, result: &HashMap<i128, Vec<(i128, i128)>>, memory : &mut HashMap<(i128, i128), i128>) -> i128{
    assert!(result.contains_key(&line));
    if memory.contains_key(&(column, line)){
        return *memory.get(&(column, line)).unwrap();
    }
    for elem in result.get(&line).unwrap(){
        if DEBUG{
        }
        if elem.0 <= column && elem.1 >= column{
            if DEBUG{
            }
            memory.insert((column ,line), elem.1);
            return elem.1;
        }
    }
    memory.insert((column ,line), -1);
    -1
}

fn col_is_inside_index(column : i128, line : i128, result: &HashMap<i128, Vec<(i128, i128)>>) -> i128{
    assert!(result.contains_key(&line));
    for (i, elem) in result.get(&line).unwrap().iter().enumerate(){
        if elem.0 <= column && elem.1 >= column{
            return i as i128;
        }
    }
    -1 
}

fn add_range_in_column(column: i128, line_1: i128, line_2: i128, result: &mut HashMap<i128, Vec<(i128, i128)>>) {
    for line in line_1.min(line_2)..line_1.max(line_2){
        if result.contains_key(&line){
            if col_is_inside_index(column, line, result) != - 1{
                continue;
            }
            result.get_mut(&line).unwrap().push((column, column));
        } else{
            result.insert(line, vec![(column, column)]);
        }
    }
}



fn add_range_in_line(line: i128, column_1: i128, column_2: i128, result: &mut HashMap<i128, Vec<(i128, i128)>>){
    let column_min = column_1.min(column_2);
    let column_max = column_1.max(column_2);

    if result.contains_key(&line){
        let sup_borne = col_is_inside_index(column_min, line, result);
        if sup_borne != -1 {
            let cur_vec = result.get_mut(&line).unwrap();
            if cur_vec.get(sup_borne as usize).unwrap().1  >= column_max{
                return;
            }
            cur_vec.get_mut(sup_borne as usize).unwrap().1 = column_max;
            return;
        }
        result.get_mut(&line).unwrap().push((column_min.min(column_max), column_min.max(column_max)));
    } else{
        result.insert(line, vec![(column_min.min(column_max), column_min.max(column_max))]);
    }
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
