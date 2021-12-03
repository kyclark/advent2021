use clap::{App, Arg};
use std::{
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
    let matches = App::new("depths")
        .version("0.1.0")
        .author("Ken Youens-Clark <kyclark@gmail.com>")
        .about("Binary strings")
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
            let mut vals: Vec<Vec<char>> = vec![];
            for line in file.lines().filter_map(Result::ok) {
                vals.push(line.chars().collect::<Vec<_>>());
            }

            let mut epsilon = vec![];
            let mut gamma = vec![];
            for i in 0..vals[0].len() {
                let bits: Vec<_> = vals.iter().map(|val| val[i]).collect();
                let ones = bits
                    .iter()
                    .filter(|&&v| v == '1')
                    .collect::<Vec<_>>()
                    .len();
                let zeros = bits.len() - ones;
                epsilon.push(if ones > zeros { '1' } else { '0' });
                gamma.push(if ones > zeros { '0' } else { '1' });
            }

            let epsilon = epsilon.iter().collect::<String>();
            let epsilon_val = isize::from_str_radix(&epsilon, 2).unwrap();
            let gamma = gamma.iter().collect::<String>();
            let gamma_val = isize::from_str_radix(&gamma, 2).unwrap();

            println!(
                "episilon {} ({}) gamma {} ({}) = {}",
                epsilon,
                epsilon_val,
                gamma,
                gamma_val,
                epsilon_val * gamma_val,
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
