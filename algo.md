$$
u_i(\sigma_i,\sigma_{-i}) = \sum_{z\in Z}\pi(\sigma_i,z)\pi(\sigma_{-i},z)u_i(z)
$$

令 $\sigma = \{s^t\}$, $s^t$表示在第t轮的一个策略分布。则上式可以改写成

$$
\sum_{z\in Z}\prod s_i^t(towards\,z) u_i(z)
$$

改写成一个超步（而不是一人一步）就好了。但是我要先赶毕设了