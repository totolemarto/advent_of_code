use std::collections::HashMap;
use std::hash::{Hash, Hasher};
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
struct Tachyon{
    row : usize,
    col : usize,
}
impl Eq for Tachyon{
}
impl PartialEq for Tachyon {
    fn eq(&self, other: &Tachyon) -> bool {
        self.col == other.col && self.row == other.row
    }
}

impl Hash for Tachyon{
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.row.hash(state);
        self.col.hash(state);
    }
}


fn add_in_memory(line: usize, column: usize, memory: &mut HashMap<Tachyon, i128>, arg: i128) {
    let tach = Tachyon{row : line, col : column};
    if memory.contains_key(&tach){
        *memory.get_mut(&tach).unwrap() += arg;
    } else{
        memory.insert(tach, arg);
    }
}

fn put_tachyon(line : usize, column : usize, matrix :  &mut [String],  memory: &mut HashMap<Tachyon, i128>, base : i128) -> i32{
    if line >= matrix.len() || column >= matrix.get(0).unwrap().len(){
        return 0;
    }
    if matrix.get(line).unwrap().chars().nth(column).unwrap() == '.'{
        let mut new_line = matrix.get_mut(line).unwrap().to_string();
        new_line.replace_range(column..column + 1, "|");
        matrix[line] = new_line;
        add_in_memory(line, column, memory, base);
        return 0;
    }
    if matrix.get(line).unwrap().chars().nth(column).unwrap() == '|'{
        add_in_memory(line, column, memory, base);
        return 0;
    }
    if matrix.get(line).unwrap().chars().nth(column).unwrap() == '^'{
        let tmp = put_tachyon(line, column - 1, matrix, memory, base);
        return  1 + put_tachyon(line, column + 1, matrix, memory, base) + tmp;
    }
    return 0;
}

fn iteration(matrix : &mut [String], line : usize,  memory: &mut HashMap<Tachyon, i128>) -> i32{
    let mut result = 0;
    for column in 0..matrix.get(0).unwrap().len(){
        if matrix.get(line).unwrap().chars().nth(column).unwrap() == '|'{
            result += put_tachyon(line + 1, column, matrix, memory, *memory.get(&Tachyon{row : line, col : column}).unwrap() );
        } else if matrix.get(line).unwrap().chars().nth(column).unwrap() == 'S'{ 
            result += put_tachyon(line + 1, column, matrix, memory, 1);
        }             
    }
    return result;
}

fn first_star(matrix : &mut [String]) -> i128{
    let mut line_begin = 0;
    let size_tot = matrix.len() - 1;
    let mut memory: HashMap<Tachyon, i128> = HashMap::new();
    let mut cur_add ;
    let mut result = 0;
    while line_begin < size_tot{ 
        cur_add = iteration(matrix, line_begin, &mut memory);
        //println!("ligne = {} -> result tmp = {}", line_begin, cur_add);
        line_begin += 1;
        result += cur_add;
    }
    for line in matrix{
        println!("{}", line);
    }
    let mut tmp_res = 0;
    for elem in memory.keys(){
        if elem.row == size_tot{
            tmp_res += memory.get(elem).unwrap();
        }
    }
    println!("nb_chemin different = {}", tmp_res);
    return result as i128;
}
//
// fn put_tachyon_2(line : usize, column : usize, charac : char) -> (Vec<Tachyon>, i128){
//     let mut result : Vec<Tachyon> = Vec::new(); 
//     let mut number = 0;
//     if charac == '.'{
//         result.push(Tachyon{row : line, col : column});
//         return (result, number); // ajouter à result
//     }
//     if  charac == '^'{
//         let mut a : Vec<Tachyon>;
//         let mut b : i128;
//         (a, b) = put_tachyon_2(line, column - 1, '.');
//         result.extend(a);
//         number += b;
//         (a, b) = put_tachyon_2(line, column + 1, '.');
//         result.extend(a);
//         number += b;
//         return (result, number + 1);
//     }
//     return (result, number);
// }
//
// fn iteration_2(charac : char, tachyon : Tachyon,  memory: &mut HashMap<Tachyon, i128>) -> (Vec<Tachyon>, i128) {
//     if memory.contains_key(&tachyon) {
//         println!("on renvoie direct sur line = {} et column = {}", tachyon.row, tachyon.col);
//         return (Vec::new(), memory[&tachyon]);
//     }
//     let a;
//     let b;
//     (a, b) = put_tachyon_2(tachyon.row + 1, tachyon.col, charac );
//     memory.insert(tachyon, b);
//     return (a, b);
// }
//
// fn second_star(matrix : Vec<String>) -> i128{
//     let mut cur_add ;
//     let mut number_possible;
//     let mut memory: HashMap<Tachyon, i128> = HashMap::new();
//     let mut memory_parent : HashMap<Tachyon, Vec<Tachyon>> = HashMap::new();
//     let mut result = 1;
//     let mut vec_tachyon : Vec<Tachyon> = vec![];
//     let mut cur_tachyon : Tachyon = Tachyon{row : 0, col : matrix[0].chars().position(|c| c == 'S').unwrap()} ;
//     let nb_rows = matrix.len();
//     let nb_cols = matrix.clone().get(0).unwrap().len();
//     vec_tachyon.push(cur_tachyon);
//     while !vec_tachyon.is_empty(){ 
//         cur_tachyon = vec_tachyon.pop().unwrap();
//         if cur_tachyon.row + 1 >= nb_rows || cur_tachyon.col >= nb_cols{
//             continue;
//         }
//         (cur_add, number_possible) = iteration_2(matrix.get(cur_tachyon.row + 1).unwrap().chars().nth(cur_tachyon.col).unwrap(), cur_tachyon, &mut memory);
//         if number_possible != 0{
//             println!(" on ajoute : {:?} car {} de result en plus sur tachyon {:?}", cur_add, number_possible, cur_tachyon);
//         }
//         for tach in cur_add.clone(){
//             if memory_parent.contains_key(&tach.clone()){
//                 memory_parent.get_mut(&tach).unwrap().push(cur_tachyon.clone());
//             } else{
//                 memory_parent.insert(tach, vec![cur_tachyon.clone()]);
//             }
//         }
//         add_to_parent(cur_tachyon, number_possible, & mut memory_parent, & mut memory);
//
//         result += number_possible;
//         vec_tachyon.extend(cur_add);
//     }
//     for line in matrix.clone(){
//
//         println!("{}", line);
//     }
//     println!("dico à la fin : \n{:?}", memory_parent);
//     println!("dico à la fin : \n{:?}", memory);
//     println!("donc pour le premier ça fait : {}", memory.get(&Tachyon{row : 0, col : matrix[0].chars().position(|c| c == 'S').unwrap()}).unwrap()); 
//     return result  as i128; 
// }
//
// fn add_to_parent(cur_tachyon: Tachyon, number_possible: i128, memory_parent: &mut HashMap<Tachyon, Vec<Tachyon>>, memory : &mut HashMap<Tachyon, i128> ) {
//     if memory_parent.contains_key(&cur_tachyon.clone()){
//         for parent in memory_parent.clone().get_mut(&cur_tachyon).unwrap(){
//             *memory.get_mut(parent).unwrap() += number_possible;
//         }
//     }
// }
//


fn main() {
    let (content, mode) = init();

    let result : i128;


    let mut split_value: Vec<String> = content.split("\n").map(|s| s.to_string()).collect();



    if mode.eq("1"){
        result = first_star(&mut split_value);
        println!("result = {}", result);
    } else {
        first_star(&mut split_value);
    }
}

