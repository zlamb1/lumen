export interface AnimationParam {
    name: string;
    type: 'bool' | 'number' | 'color';
    value: string | boolean | number;
};

export interface Animation {
    name: string;
    paused: boolean;
    params: AnimationParam[];
};