use clap::{App, Arg};
use std::{
    error::Error,
    fs::File,
    io::{self, BufRead, BufReader},
    mem,
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

            let oxygen = calc(&vals, true);
            let co2 = calc(&vals, false);
            if let (Some(o), Some(c)) = (oxygen, co2) {
                let o_val = isize::from_str_radix(&o, 2).unwrap();
                let c_val = isize::from_str_radix(&c, 2).unwrap();
                println!(
                    "oxygen {} co2 {} = {}",
                    o_val,
                    c_val,
                    o_val * c_val
                );
            }
        }
    }

    Ok(())
}

// --------------------------------------------------
fn calc(vals: &Vec<Vec<char>>, most_wanted: bool) -> Option<String> {
    let mut copied: Vec<Vec<char>> = vals.iter().cloned().collect();

    for i in 0..vals[0].len() {
        let bits: Vec<_> = copied.iter().map(|val| val[i]).collect();
        let ones =
            bits.iter().filter(|&&v| v == '1').collect::<Vec<_>>().len();
        let zeros = bits.len() - ones;
        let (most_common, least_common) = if ones >= zeros {
            ('1', '0')
        } else {
            ('0', '1')
        };
        let cmp = if most_wanted {
            most_common
        } else {
            least_common
        };
        let mut filtered: Vec<Vec<char>> =
            copied.iter().filter(|val| val[i] == cmp).cloned().collect();

        if filtered.len() == 1 {
            return Some(filtered[0].iter().collect::<String>());
        }
        copied = mem::take(&mut filtered);
    }

    None
}

// --------------------------------------------------
fn open(filename: &str) -> MyResult<Box<dyn BufRead>> {
    match filename {
        "-" => Ok(Box::new(BufReader::new(io::stdin()))),
        _ => Ok(Box::new(BufReader::new(File::open(filename)?))),
    }
}
