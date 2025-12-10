use std::collections::HashMap;
use std::env;
use std::fs;
use std::cell::RefCell;

thread_local!(static DEBUG: RefCell<bool> = RefCell::new(true));

#[derive(Debug, Clone, Copy)]
struct JunctionBoxe{
    x : i128,
    y : i128,
    z : i128,
    circuits : i32,
    pos : usize,
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

fn create_junction(matrix: Vec<String>) -> Vec<JunctionBoxe> {
    let mut result : Vec<JunctionBoxe> = Vec::new();
    let mut i = 0;
    for line in matrix{
        if line.eq(""){
            continue;
        }
        let mut values = line.split(",");
        let x = values.next().unwrap().parse::<i128>().unwrap();
        let y = values.next().unwrap().parse::<i128>().unwrap();
        let z = values.next().unwrap().parse::<i128>().unwrap();
        result.push(JunctionBoxe{x, y, z, circuits :  -1, pos : i});
        i += 1;
    }
    return result;

}


fn first_star(matrix : Vec<String>) -> i128{
    let mut vec_junction = create_junction(matrix);
    let mut matrix_dist = create_matrix_dist(&vec_junction);

    let nb_iteration;
    if vec_junction.len() < 100{
        nb_iteration = 10;
    } else {
        nb_iteration = 1000;
    }
    let nb_maxi = 3;
    let mut result = 1;

    let circuit_to_junction = iterate(&mut vec_junction, &mut matrix_dist, nb_iteration);

    // println!("A la fin on a :\n{:?}", circuit_to_junction);
    let mut vec_size : Vec<usize> = Vec::new();
    for (_key, elem) in &circuit_to_junction{
        vec_size.push(elem.len());
        // println!("on a une taille de {} sur le circuit {}", elem.len(), key);
    }
    vec_size.sort_by(|a, b| b.partial_cmp(a).unwrap());
    for i in 0..nb_maxi{
        result *= vec_size[i];
    }
    return result as i128;
}

fn second_star(matrix : Vec<String>) -> i128{
    let mut vec_junction = create_junction(matrix);
    let mut matrix_dist = create_matrix_dist(&vec_junction);


    let (elem_1, elem_2, nb_iter) = iterate_2(&mut vec_junction, &mut matrix_dist);

    println!("Ca prend {} iterations", nb_iter);
    return elem_1.x * elem_2.x;
}

fn merge_two_junction(vec_junction: &mut Vec<JunctionBoxe>, matrix_dist: & mut Vec<Vec<i128>>, circuit_to_junction : &mut HashMap<i32, Vec<JunctionBoxe>>, new_circuit : & mut i32) -> (usize, usize){
    let (line, column) = get_pair_with_min_distance(&matrix_dist);
    // println!("on va appairer les valeures {:?} et {:?}", vec_junction[line], vec_junction[column]);
    matrix_dist[line][column] = -1; 
    if vec_junction[line].circuits == vec_junction[column].circuits && vec_junction[line].circuits == -1{
        vec_junction[line].circuits = *new_circuit;
        vec_junction[column].circuits = *new_circuit;
        circuit_to_junction.insert(*new_circuit, vec![vec_junction[line], vec_junction[column]]);
        *new_circuit += 1;
    } else if -1 ==  vec_junction[column].circuits || vec_junction[line].circuits == -1{
        if vec_junction[line].circuits == -1{
            vec_junction[line].circuits = vec_junction[column].circuits;
            circuit_to_junction.get_mut(&vec_junction[column].circuits).unwrap().push(vec_junction[line]);
        } else{
            vec_junction[column].circuits = vec_junction[line].circuits;
            circuit_to_junction.get_mut(&vec_junction[line].circuits).unwrap().push(vec_junction[column]);
        }
    } else if  vec_junction[line].circuits == vec_junction[column].circuits {
        return (0, 0);
    } else {
        assert_ne!(vec_junction[line].circuits, -1);
        for junction in circuit_to_junction.remove(&vec_junction[line].circuits).unwrap().iter_mut(){
            vec_junction[junction.pos].circuits = vec_junction[column].circuits;
            junction.circuits = vec_junction[column].circuits;
            circuit_to_junction.get_mut(&vec_junction[column].circuits).unwrap().push(*junction);
        }
    }
    return (line , column );
}

fn iterate_2(vec_junction: &mut Vec<JunctionBoxe>, matrix_dist: & mut Vec<Vec<i128>>) -> (JunctionBoxe, JunctionBoxe, i32){
    let mut circuit_to_junction : HashMap<i32, Vec<JunctionBoxe>> = HashMap::new();
    let mut new_circuit = 0;
    let mut finish = false;
    let mut line = 0;
    let mut column = 0;
    let mut nb_iter = 0;
    while !finish{
        nb_iter += 1;
        (line, column) = merge_two_junction(vec_junction, matrix_dist, &mut circuit_to_junction, & mut new_circuit);
        if line == column {
            continue;
        }
        finish = circuit_to_junction.get(&vec_junction[line].circuits).unwrap().len() == vec_junction.len();
    }
    return (vec_junction[line], vec_junction[column], nb_iter);
}

fn iterate(vec_junction: &mut Vec<JunctionBoxe>, matrix_dist: & mut Vec<Vec<i128>>, nb_iteration: i32) -> HashMap<i32, Vec<JunctionBoxe>>{
    let mut circuit_to_junction : HashMap<i32, Vec<JunctionBoxe>> = HashMap::new();
    let mut new_circuit = 0;
    for _i in 0..nb_iteration{
        // println!("on va appairer les valeures {:?} et {:?}", vec_junction[line], vec_junction[column]);
        merge_two_junction(vec_junction, matrix_dist, &mut circuit_to_junction, & mut new_circuit);
    }
    return circuit_to_junction;
}

fn get_pair_with_min_distance(matrix_dist: &Vec<Vec<i128>>) -> (usize, usize) {
    let mut result_line = 0;
    let mut result_column = 1;
    let mut mini = matrix_dist[0][1];
    for (line, content) in matrix_dist.iter().enumerate(){
        for (column, dist) in content.iter().enumerate(){ // la matrice sera toujours symétrique ->
                                                          // on peut couper en deux
            if line.le(&column){
                continue;
            }
            if *dist < mini && *dist > 0{
                mini = *dist; 
                result_line = line;
                result_column = column;
            }
        }
    }

    return (result_line, result_column);

}

fn create_matrix_dist(vec_junction: &Vec<JunctionBoxe>) -> Vec<Vec<i128>> {
    let mut result : Vec<Vec<i128>> = Vec::new();
    for (i, elem_1) in vec_junction.iter().enumerate(){
        result.push(Vec::new());
        for elem_2 in vec_junction.iter(){
            result[i].push(get_distance(elem_1, elem_2));
        }
    }

    return result;

}

fn get_distance(elem_1: &JunctionBoxe, elem_2: &JunctionBoxe) -> i128 {
    return (elem_1.x - elem_2.x).pow(2) + (elem_1.y - elem_2.y).pow(2) + (elem_1.z - elem_2.z).pow(2);
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

