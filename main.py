from apis.data_explore import data_explore
from apis.data_modeling import data_modeling


def main():
    df = data_explore()
    # data_modeling(df)


if __name__ == '__main__':
    main()

