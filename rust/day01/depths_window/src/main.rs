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
    window: usize,
}

// --------------------------------------------------
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
        .arg(
            Arg::with_name("window")
                .short("w")
                .long("window")
                .value_name("WINDOW")
                .help("Window size")
                .default_value("3"),
        )
        .get_matches();

    let window = matches
        .value_of("window")
        .map(parse_positive_int)
        .transpose()
        .map_err(|e| format!("Invalid window \"{}\"", e))?;

    Ok(Config {
        filename: matches.value_of("filename").unwrap().to_string(),
        window: window.unwrap(),
    })
}

// --------------------------------------------------
fn parse_positive_int(val: &str) -> MyResult<usize> {
    match val.parse() {
        Ok(n) if n > 0 => Ok(n),
        _ => Err(From::from(val)),
    }
}

// --------------------------------------------------
#[test]
fn test_parse_positive_int() {
    // 3 is an OK integer
    let res = parse_positive_int("3");
    assert!(res.is_ok());
    assert_eq!(res.unwrap(), 3);

    // Any string is an error
    let res = parse_positive_int("foo");
    assert!(res.is_err());
    assert_eq!(res.unwrap_err().to_string(), "foo".to_string());

    // A zero is an error
    let res = parse_positive_int("0");
    assert!(res.is_err());
    assert_eq!(res.unwrap_err().to_string(), "0".to_string());
}

// --------------------------------------------------
fn main() -> MyResult<()> {
    let args = get_args()?;
    match open(&args.filename) {
        Err(err) => eprintln!("{}: {}", args.filename, err),
        Ok(file) => {
            let mut num_increased = 0;
            let mut prev = vec![];
            for line in file.lines() {
                let line = line?;
                if let Ok(num) = line.parse::<usize>() {
                    if prev.len() == args.window {
                        let prev_sum: usize = prev.iter().sum();
                        prev.remove(0);
                        prev.push(num);
                        let this_sum: usize = prev.iter().sum();
                        if prev_sum < this_sum {
                            num_increased += 1;
                        }
                    } else {
                        prev.push(num);
                    }
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
