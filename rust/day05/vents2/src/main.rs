use clap::{App, Arg};
use itertools::{
    EitherOrBoth::{Both, Left, Right},
    Itertools,
};
use regex::Regex;
use std::{
    collections::HashMap,
    error::Error,
    fs::File,
    io::{self, BufRead, BufReader},
};

type MyResult<T> = Result<T, Box<dyn Error>>;

#[derive(Debug)]
pub struct Config {
    filename: String,
}

// --------------------------------------------------
pub fn get_args() -> MyResult<Config> {
    let matches = App::new("vents")
        .version("0.1.0")
        .author("Ken Youens-Clark <kyclark@gmail.com>")
        .about("Map vents")
        .arg(
            Arg::with_name("filename")
                .value_name("FILE")
                .help("Input data file")
                .default_value("-"),
        )
        .get_matches();

    Ok(Config {
        filename: matches.value_of("filename").unwrap().to_string(),
    })
}

// --------------------------------------------------
fn main() -> MyResult<()> {
    let args = get_args()?;
    match open(&args.filename) {
        Err(err) => eprintln!("{}: {}", args.filename, err),
        Ok(file) => {
            let re = Regex::new(r"^(\d+),(\d+)\s+->\s+(\d+),(\d+)$").unwrap();
            let mut grid = HashMap::new();
            for line in file.lines().filter_map(Result::ok) {
                if let Some(caps) = re.captures(&line) {
                    //println!("{:?}", caps);
                    let x1 = caps
                        .get(1)
                        .map(|v| v.as_str().parse::<usize>().unwrap())
                        .unwrap();
                    let y1 = caps
                        .get(2)
                        .map(|v| v.as_str().parse::<usize>().unwrap())
                        .unwrap();
                    let x2 = caps
                        .get(3)
                        .map(|v| v.as_str().parse::<usize>().unwrap())
                        .unwrap();
                    let y2 = caps
                        .get(4)
                        .map(|v| v.as_str().parse::<usize>().unwrap())
                        .unwrap();

                    let xs: Vec<_> = if x1 < x2 {
                        (x1..=x2).collect()
                    } else {
                        (x2..=x1).rev().collect()
                    };
                    let ys: Vec<_> = if y1 < y2 {
                        (y1..=y2).collect()
                    } else {
                        (y2..=y1).rev().collect()
                    };
                    //println!("x1 {} x2 {} = {:?}", x1, x2, xs);
                    //println!("y1 {} y2 {} = {:?}", y1, y2, ys);

                    let points: Vec<_> = xs
                        .iter()
                        .zip_longest(&ys)
                        .map(|v| match v {
                            Both(a, b) => (*a, *b),
                            Left(a) => (*a, ys[0]),
                            Right(b) => (xs[0], *b),
                        })
                        .collect();
                    //println!("points = {:?}", points);

                    for (x, y) in points {
                        let pt =
                            grid.entry((x.clone(), y.clone())).or_insert(0);
                        *pt += 1;
                    }
                }
            }

            println!(
                "{:?}",
                grid.into_values()
                    .filter(|&v| v > 1)
                    .collect::<Vec<_>>()
                    .len()
            );
        }
    }

    Ok(())
}

// --------------------------------------------------
fn open(filename: &str) -> MyResult<Box<dyn BufRead>> {
    match filename {
        "-" => Ok(Box::new(BufReader::new(io::stdin()))),
        _ => Ok(Box::new(BufReader::new(File::open(filename)?))),
    }
}
