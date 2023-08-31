from typing import Iterable, Tuple, Any, Callable, Optional

from . import MemoryMixin


class MultiValueMergerMixin(MemoryMixin):
    def __init__(self, *args, element_limit=5, annotation_limit=40, top_func=None, phi_maker=None, **kwargs):
        self._element_limit = element_limit
        self._annotation_limit = annotation_limit
        self._top_func: Callable = top_func
        self._phi_maker: Optional[Callable] = phi_maker

        super().__init__(*args, **kwargs)

    def _merge_values(self, values: Iterable[Tuple[Any, Any]], merged_size: int, **kwargs):
        values_set = {v for v, _ in values}
        if self._phi_maker is not None:
            phi_var = self._phi_maker(values_set)
            if phi_var is not None:
                return {phi_var}

        # try to merge it in the traditional way
        if len(values_set) > self._element_limit:
            top_val = self._top_func(merged_size * self.state.arch.byte_width)
            # migrate annotations
            annotations = []
            annotations_set = set()
            for v in values_set:
                for anno in v.annotations:
                    if anno not in annotations_set:
                        annotations.append(anno)
                        annotations_set.add(anno)
            if annotations:
                top_val = top_val.annotate(*annotations[: self._annotation_limit])
            merged_val = {top_val}
        else:
            merged_val = values_set
        return merged_val

    def copy(self, memo=None):
        copied = super().copy(memo)
        copied._element_limit = self._element_limit
        copied._annotation_limit = self._annotation_limit
        copied._top_func = self._top_func
        copied._phi_maker = self._phi_maker
        return copied
