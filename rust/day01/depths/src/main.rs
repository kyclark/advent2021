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

pub fn get_args() -> MyResult<Config> {
    let matches = App::new("depths")
        .version("0.1.0")
        .author("Ken Youens-Clark <kyclark@gmail.com>")
        .about("Detect depths increasing/decreasing")
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

fn main() -> MyResult<()> {
    let args = get_args()?;
    match open(&args.filename) {
        Err(err) => eprintln!("{}: {}", args.filename, err),
        Ok(file) => {
            let mut num_increased = 0;
            let mut prev: Option<usize> = None;
            for line in file.lines() {
                let line = line?;
                if let Ok(num) = line.parse::<usize>() {
                    if let Some(val) = prev {
                        println!(
                            "{} {}creased",
                            num,
                            if val < num { "in" } else { "de" }
                        );
                        if val < num {
                            num_increased += 1;
                        }
                    }
                    prev = Some(num);
                }
            }
            println!("{} increased", num_increased);
        }
    }

    Ok(())
}

fn open(filename: &str) -> MyResult<Box<dyn BufRead>> {
    match filename {
        "-" => Ok(Box::new(BufReader::new(io::stdin()))),
        _ => Ok(Box::new(BufReader::new(File::open(filename)?))),
    }
}
